# -- coding utf-8 --
# @Time     2022/5/8 上午12:22
# @Author   dicardo
# @File     production.py
# @Software PyCharm

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easy_lottery.settings.production')

application = get_wsgi_application()
