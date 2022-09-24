# -*- coding: utf-8 -*-
# @Time    : 2021/7/6 10:54
# @Author  : dicardo
# @File    : tasks.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    return x + y
