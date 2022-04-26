"""
WSGI config for Note_Cloud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Note_Cloud.settings')

application = get_wsgi_application()


from django.contrib.staticfiles.handlers import StaticFilesHandler # 添加模块
# 修改 application = get_wsgi_application()
application = StaticFilesHandler(get_wsgi_application())