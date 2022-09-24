# -- coding utf-8 --
# @Time     2021/6/27 21:22
# @Author   dicardo
# @File     production.py
# @Software PyCharm

from .base import *

DEBUG = False
WSGI_APPLICATION = 'easy_lottery.config.wsgi.production.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ['mysql_host'],
        'PORT': os.environ['mysql_port'],
        'NAME': os.environ['mysql_name'],
        'USER': os.environ['mysql_user'],
        'PASSWORD': os.environ['mysql_pwd'],
        'OPTIONS': {'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'}
    }
}
