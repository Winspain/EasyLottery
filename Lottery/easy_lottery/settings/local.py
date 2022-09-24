# -- coding utf-8 --
# @Time     2021/6/27 21:22
# @Author   dicardo
# @File     local.py
# @Software PyCharm

from .base import *

SECRET_KEY = 'django-insecure-h5^2mae#oec%^psk=d4=(pxn34v-*kfq7r84+%fq=3+pys5(&p'

# WSGI_APPLICATION = 'easy_lottery.config.wsgi.local.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
