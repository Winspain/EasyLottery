# -*- coding: utf-8 -*-
# @Time    : 2021/7/5 14:42
# @Author  : dicardo
# @File    : local.py
# @Software: PyCharm

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "easy_lottery.settings.production")

app = Celery("easy_lottery")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['celery_tasks'])
