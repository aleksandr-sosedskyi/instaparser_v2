import requests
import json 
import random 
import traceback

from celery import shared_task

from django.conf import settings

from core.models import InstaUser, Process, Log, Controller, APIKey, SpeedLog, UserHistory
from core.utils import parse_user_data


class InvalidResponseException(Exception):
    def __init__(self, status_code, text):
        message = f"Invalid response from API. ({status_code}) : {text}"
        super().__init__(message)


def process_completed_task(task):
    response = requests.get(settings.API_URL + f"?key={task.api_key}&mode=result&tid={task.tid}")
    if response.status_code == 200:
        users_list = parse_user_data(response.text.replace('\n', ' '))
        if not users_list:
            task.delete()
            return
        for user in users_list: 
            status = InstaUser.UNHACKABLE
            if len(user) != 8:
                raise ValueError(f"User has invalid data - {user}")
            if user[6] == "0":
                email = None
            else:
                email = user[6]
                if "yandex" in email or "rambler" in email:
                    status = InstaUser.RIGHT_EMAIL
            if not user[1]:
                continue
            obj, created = InstaUser.objects.get_or_create(
                ig_id=user[0],
                defaults={
                    'ig_id':user[0],
                    'username':user[1],
                    'subscribers':int(user[2]) if user[2] else None,
                    'subscriptions':int(user[3]) if user[3] else None,
                    'name':user[4] if user[4] and user[4] != "0" else None,
                    'phone':user[5] if user[5] and user[5] != "0" else None,
                    'email':user[6] if user[6] and user[6] != "0" else None,
                    'city':user[7] if user[7] and user[7] != "0" else None,
                    'status':status,
                    'tid': task.tid,
                    'api_key': task.api_key
                }
            )
            if not created:
                old_phone, old_email, old_city = obj.phone, obj.email, obj.city
                obj.username = user[1]
                obj.subscribers = int(user[2]) if user[2]  else obj.subscribers
                obj.subscriptions = int(user[3]) if user[3] else obj.subscriptions
                obj.name = user[4] if user[4] and user[4] != "0" else obj.name 
                obj.phone = user[5] if user[5] and user[5] != "0" else obj.phone 
                obj.email = user[6] if user[6] and user[6] != "0" else obj.email 
                obj.city = user[7] if user[7] and user[7] != "0" else obj.city 
                obj.status = InstaUser.RIGHT_EMAIL if obj.email and ('rambler' in obj.email or 'yandex' in obj.email) else InstaUser.UNHACKABLE
                obj.tid = task.tid
                obj.api_key = task.api_key
                obj.save()
                if [old_phone, old_email, old_city] != [obj.phone, obj.email, obj.city]:
                    UserHistory.objects.create(user=obj, email=obj.email, phone=obj.phone, city=obj.city)
    else:
        raise InvalidResponseException(response.status_code, response.text)
    user = task.user
    user.is_processed = True
    user.save()
    SpeedLog.objects.create(count=task.count)
    task.delete()


@shared_task
def parse():
    controller, created = Controller.objects.get_or_create()
    if not controller.is_finished or controller.is_stopped:
        return
    controller.is_finished = False
    controller.save()
    queryset = Process.objects.all()
    for api_key in APIKey.objects.values_list('api_key', flat=True):
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
                        user.is_invalid_process = True
                        user.is_scrapping = False
                        user.save()
                        task.delete()
                        tasks_count -= 1
                    elif data['tid_status'] == 'completed':
                        task.count = data['count']
                        task.save()
                        try:
                            if data['count'] == 0 and task.user.subscribers != 0:
                                user = task.user
                                user.is_scrapping = False
                                user.save()
                                SpeedLog.objects.create(count=task.count)
                                task.delete()
                            else:
                                process_completed_task(task)
                        except Exception as e:
                            message = traceback.format_exc()
                            Log.objects.create(tid=task.tid, api_key=api_key, action=Log.CREATE_USERS, message=message)
                        tasks_count -= 1
                else:
                    raise InvalidResponseException(response.status_code, response.text)
            except Exception as e:
                message = traceback.format_exc()
                Log.objects.create(message=message, api_key=api_key, tid=task.tid, action=Log.CHECK_API)
        
        try:
            for i in range(0, 3-tasks_count):
                if not (users := InstaUser.objects.get_users_to_parse()).exists():
                    break
                user_to_parse = random.choice(users)
                response = requests.get(settings.API_URL + f"?key={api_key}&mode=create&type=p1&act=1&spec=1,2&limit=10000&web=1&links={user_to_parse.username}&dop=1,2,3,5,8")
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
            message = traceback.format_exc()
            Log.objects.create(message=message, api_key=api_key, action=Log.CREATE_TASK)
    controller.is_finished = True
    controller.save()


@shared_task
def check_api_keys_task(pk):
    obj = APIKey.objects.get(pk=pk)
    response = requests.get(f"{settings.API_URL}?key={obj.api_key}&mode=delete&tid=0")
    if response.status_code == 200 and response.json().get('text') != "invalid key":
        obj.active = True
        obj.save()
    else:
        Process.objects.filter(api_key=obj.api_key).delete()
        obj.active = False
        obj.save()
