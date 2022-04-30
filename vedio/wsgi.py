"""
WSGI config for Note_Cloud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from sched import scheduler

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vedio.settings')

application = get_wsgi_application()


from django.contrib.staticfiles.handlers import StaticFilesHandler # 添加模块
# 修改 application = get_wsgi_application()
application = StaticFilesHandler(get_wsgi_application())

import os

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


# 定时任务, 清空session数据库,这个库不清的话,会不停的增大
@scheduler.scheduled_job(trigger='interval', days=1,start_date='2022-05-02 20:08:00', id='clear_session')

def clear_session_job():
    print('clear session data base')
    # 命令行执行python manage.py clearsessions,可以清除已经失效的session
    os.system('python manage.py clearsessions')


scheduler.start()

