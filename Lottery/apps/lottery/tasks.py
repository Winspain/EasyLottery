# -- coding utf-8 --
# @Time     2022/10/2 23:46
# @Author   dicardo
# @File     tasks.py
# @Software PyCharm

from __future__ import absolute_import, unicode_literals

import requests
from celery import shared_task


@shared_task
def crawl_by_500():
    url = 'http://127.0.0.1:8888/easyLottery/v1/lottery/craw'
    response_data = requests.post(url).json()
    return response_data['data']
