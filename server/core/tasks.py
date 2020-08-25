import requests
import json 

from celery import shared_task
from core.models import InstaUser, Process, Log
from django.conf import settings

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class InvalidResponseException(Exception):
    def __init__(self, status_code, text):
        message = f"Invalid response from API. ({status_code}) : {text}"
        super().__init__(message)


def process_completed_task(task):
    response = requests.get(settings.API_URL + f"?key={task.api_key}&mode=result&tid={task.tid}")
    if response.status_code == 200:
        users_list = [x.split(':') for x in response.text.split(' ')]
        status = InstaUser.UNHACKABLE
        for user in users_list: 
            if len(user) != 8:
                logger.info(user)
            if user[6] == "0":
                email = None
            else:
                email = user[6]
                if "yandex" in email or "rambler" in email:
                    status = InstaUser.RIGHT_EMAIL

            obj, created = InstaUser.objects.get_or_create(
                ig_id=user[0],
                username=user[1],
                subscribers=user[2] if user[2] != 0 else None,
                subscriptions=user[3] if user[3] != "0" else None,
                name=user[4] if user[4] != "0" else None,
                phone=user[5] if user[5] != "0" else None,
                email=user[6] if user[6] != "0" else None,
                city=user[7] if user[7] != "0" else None,
                status=status
            )
            if not created:
                username = user[1]
                obj.subscribers = user[2]
                obj.subscriptions = user[3]
                obj.name = user[4] if user[4] else obj.name 
                obj.phone = user[5] if user[5] else obj.phone 
                obj.city = user[6] if user[6] else obj.city 
                obj.name = user[7] if user[7] else obj.name 
                obj.save()
    else:
        raise InvalidResponseException(response.status_code, response.text)
    task.delete()


@shared_task
def parse():
    queryset = Process.objects.all()
    for api_key in settings.API_KEYS:
        tasks = queryset.filter(api_key=api_key)
        tasks_count = tasks.count()
        for task in tasks:
            try:
                response = requests.get(settings.API_URL + f"?key={api_key}&mode=status&tid={task.tid}")
                if response.status_code == 200 and (data := response.json()).get('status') == 'ok':
                    if data['tid_status'] == 'in progress':
                        task.count = data['count']
                        task.save()
                    elif data['tid_status'] == 'error':
                        user = task.user
                        user.status = InstaUser.INVALID
                        user.save()
                        task.delete()
                        tasks_count -= 1
                    elif data['tid_status'] == 'completed':
                        try:
                            process_completed_task(task)
                        except Exception as e:
                            Log.objects.create(task=task, action=Log.CREATE_USERS, message=e)
                        tasks_count -= 1
                else:
                    raise InvalidResponseException(response.status_code, response.text)
            except Exception as e:
                Log.objects.create(message=e, task=task, action=Log.CHECK_API)
        
        try:
            for i in range(0, 3-tasks_count):
                if not (users := InstaUser.get_users_to_parse()).exists():
                    break
                user_to_parse = users.first()
                response = requests.get(settings.API_URL + f"?key={api_key}&mode=create&type=p1&act=1&spec=1,2&limit=10000&web=1&links={user_to_parse.username}")
                if response.status_code == 200 and (data := response.json()).get('status') == 'ok':
                    Process.objects.create(
                        user=user_to_parse,
                        tid=data['tid'],
                        api_key=api_key,
                    )
                    user_to_parse.is_scrapping = True
                    user_to_parse.save()
                else:
                    user_to_parse.is_invalid_process = True
                    user_to_parse.save()
                    raise InvalidResponseException(response.status_code, response.text)
        except Exception as e:
            Log.objects.create(message=e, action=Log.CREATE_TASK)
            