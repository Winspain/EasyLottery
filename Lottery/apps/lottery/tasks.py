# -- coding utf-8 --
# @Time     2022/10/2 23:46
# @Author   dicardo
# @File     tasks.py
# @Software PyCharm

from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def add():
    return 3
