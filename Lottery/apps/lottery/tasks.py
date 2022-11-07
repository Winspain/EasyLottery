# -- coding utf-8 --
# @Time     2022/10/2 23:46
# @Author   dicardo
# @File     tasks.py
# @Software PyCharm

from __future__ import absolute_import, unicode_literals

import json
import time

import requests
from celery import shared_task

from lottery.models import LotteryInfo, LotterySelectInfo, LotteryWebhookInfo
from lottery.serializers.lottery_serializer import Lottery500Serializer
from lottery.service.get_lottery import get_latest_number_by_500
from lottery.service.lottery_rules import lottery_compare, lottery_rule


@shared_task
def crawl_by_500():
    url = 'http://127.0.0.1:8888/easyLottery/v1/lottery/craw'
    response_data = requests.post(url).json()
    return response_data


@shared_task
def notice_dingding():
    url = 'http://127.0.0.1:8888/easyLottery/v1/lottery/compare'
    response_data = requests.get(url).json()


@shared_task
def crawl_notice_task():
    begin_time = time.time()

    lottery_queryset = LotteryInfo.objects.exclude(isDeleted=True)
    select_queryset = LotterySelectInfo.objects.exclude(isDeleted=True)
    webhook_queryset = LotteryWebhookInfo.objects.exclude(isDeleted=True)

    while True:
        latest_number = get_latest_number_by_500()
        draw_num = latest_number['drawNum']
        # if not lottery_queryset.filter(drawNum=draw_num).exists():
        if lottery_queryset.filter(drawNum=draw_num).exists():  # debug暂时使用
            break
        if time.time() - begin_time > 3600 * 4:
            return '运行超过4小时,自动停止'
        # serializer = Lottery500Serializer(data=latest_number)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

    draw_info = lottery_queryset.latest('drawTime')
    draw_num = draw_info.drawNum
    draw_time = draw_info.drawTime
    draw_list = [draw_info.frontNum1, draw_info.frontNum2, draw_info.frontNum3, draw_info.frontNum4, draw_info.frontNum5, draw_info.backNum1, draw_info.backNum2]
    draw_list_without_quotes = str(draw_list).replace("'", ' ')  # 格式和自选号码保持一致,填充空格
    # TODO 后续根据用户分别筛选
    select_info = select_queryset.filter(createdBy='1')
    draw_result_list = list()
    select_str = str()
    for _ in select_info:
        select_list = [_.frontNum1, _.frontNum2, _.frontNum3, _.frontNum4, _.frontNum5, _.backNum1, _.backNum2]
        select_str += f'{select_list}\n'
        front_number, back_number = lottery_compare(select_list, draw_list)
        draw_result_list.append(lottery_rule(front_number, back_number))

    '''替换单引号为空格,若不填充空格,手机端显示无换行'''
    select_format = select_str.replace("'", ' ')
    # TODO 后续根据用户分别通知
    headers = {
        'Content-Type': 'application/json'
    }
    hook_url = webhook_queryset.filter(createdBy='1').values_list('hookUrl').first()[0]
    push_text = f'## 开奖期号:{draw_num}\n ## 开奖时间:{draw_time}\n ## 开奖结果:{draw_result_list}\n #### 开奖号码:\n{draw_list_without_quotes}\n' \
                f'#### 自选号码:\n{select_format}'
    payload = json.dumps({
        'msgtype': 'markdown',
        'markdown': {
            'title': f'{draw_num}',
            'text': push_text  # 去除引号
        }
    })
    notice_dingding = requests.post(hook_url, data=payload, headers=headers)


def test():
    return 'test'
