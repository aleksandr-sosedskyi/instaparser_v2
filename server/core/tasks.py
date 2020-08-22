import requests
import json 

from celery import shared_task
from core.models import InstaUser, Process, Log
from django.conf import settings


def process_completed_task(task):
    response = requests.get(settings.API_URL + f"key={api_key}&mode=result&tid={task.tid}")
    if response.status_code == 200:
        users_list = [x.split(':') for x in response.text.split(' ')]
        for user in users_list:
            InstaUser.objects.create(
                ig_id=user[0],
                username=user[1],
                subscribers=users[2],
                subscriptions=users[3],
                name=users[4] if users[4] != "0" else None,
            )
    user = task.user
    user.status = InstaUser.UNHACKABLE
    user.save()
    task.delete()


@shared_task
def parse():
    queryset = Process.objects.all()
    for api_key in settings.API_KEYS:
        tasks = queryset.filter(api_key=api_key)
        for task in tasks:
            try:
                response = requests.get(settings.API_URL + f"key={api_key}&mode=status&tid={task.tid}")
                if response.status_code == 200 and (data := response.json()).get('status') == 'ok':
                    if data['tid_status'] == 'in progress':
                        task.count = data['count']
                        task.save()
                    elif data['tid_status'] == 'error':
                        user = task.user
                        user.status = InstaUser.INVALID
                        user.save()
                        task.delete()
                    elif data['tid_status'] == 'completed':
                        process_completed_task(task)
            except Exception as e:
                Log.objects.create(message=e, task=task)
