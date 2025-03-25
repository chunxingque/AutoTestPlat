# -*- coding: utf-8 -*-

from celery import shared_task

@shared_task()
def task__one():
    print(11111)

    
@shared_task()
def task__send_email_param(email):
    print("send email to %s" % email)
    return "success"

@shared_task()
def task__send_email():
    print("send email to xxx")
    return "success"
