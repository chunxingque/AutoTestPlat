
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import json
from datetime import timedelta

import pytz
from datetime import datetime

import pytz
from django.http import JsonResponse
from django_celery_beat.models import ClockedSchedule, PeriodicTask, CrontabSchedule, IntervalSchedule

from dvadmin3_celery.tasks import task__send_email

def celery_add(request):
    res=task__send_email.delay("example@qq.com")
    return HttpResponse(res)

def clock_task(request):
    # 任务名
    task_name = 'clock_task'
    now_time = datetime.now()
    execute_time = now_time + timedelta(seconds=30) - timedelta(hours=8)
    # 创建任务的执行时间
    clock = ClockedSchedule.objects.get_or_create(clocked_time=execute_time)
    
    # 创建或更新指定时间执行的celery任务
    PeriodicTask.objects.update_or_create(
        name=task_name,  # 任务名，尽量保证唯一性
        defaults={
            'task': 'dvadmin3_celery.tasks.task__send_email_param',
            'clocked': clock[0],
            'one_off': True,  # 在任务执行完一次后关闭该任务
            'enabled': True,  # 开启任务
            'args': json.dumps(["example@qq.com"]),  # 参数列表，必须是json格式的数组
        }
    )
    return JsonResponse({'message': '200', 'task_name': task_name, 'execute_time': execute_time})


def interval_task(request):
    # 任务名
    task_name = 'interval_task'
    # 任务的执行时间
    schedule, created = IntervalSchedule.objects.update_or_create(
    every=20,
    period=IntervalSchedule.SECONDS)   # 按分钟间隔执行 
            
    PeriodicTask.objects.update_or_create(
        name=task_name,  # 任务名，尽量保证唯一性
        defaults={
            'task': 'dvadmin3_celery.tasks.task__send_email',
            'interval': schedule, 
            'enabled': True,  # 开启任务
            'args': json.dumps(["example@qq.com"]),  # 参数列表，必须是json格式的数组
        }
    )
    return JsonResponse({'message': '200', 'task_name': task_name})

def crontab_task(request):
    # 任务名
    task_name = 'crontab_task'
    # 任务的执行时间
    schedule, created = CrontabSchedule.objects.update_or_create(
        minute="03",
        hour="17",   
        day_of_week="*",
        day_of_month='*',
        month_of_year='*',
        timezone=pytz.timezone("Asia/Shanghai"),
    )
            
    PeriodicTask.objects.update_or_create(
        name=task_name,
        task='dvadmin3_celery.tasks.task__send_email',
        crontab = schedule,
        enabled = True,  # 开启任务
        # args = json.dumps(["example@qq.com"]),  # 参数列表，必须是json格式的数组
        kwargs=json.dumps({'email': 'example@qq.com'}),
    )
    return JsonResponse({'message': '200', 'task_name': task_name})