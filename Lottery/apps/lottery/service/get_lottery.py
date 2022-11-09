# -- coding utf-8 --
# @Time     2022/10/2 19:11
# @Author   dicardo
# @File     get_lottery.py
# @Software PyCharm
import json

import bs4
import requests

from lottery.models import LotteryWebhookInfo


def get_latest_number_by_500():
    url_500 = 'http://datachart.500.com/dlt/history/history.shtml'
    response_500 = requests.get(url_500)
    if not response_500.status_code == 200:
        return False
    soup_500 = bs4.BeautifulSoup(response_500.text, "html.parser")
    body_500 = soup_500.find('tbody', id="tdata")
    lottery_tr = body_500.find_all('tr')
    lottery_td = lottery_tr[0].find_all('td')
    return {
        'drawNum': lottery_td[0].text,
        'frontNum1': lottery_td[1].text,
        'frontNum2': lottery_td[2].text,
        'frontNum3': lottery_td[3].text,
        'frontNum4': lottery_td[4].text,
        'frontNum5': lottery_td[5].text,
        'backNum1': lottery_td[6].text,
        'backNum2': lottery_td[7].text,
        'drawTime': lottery_td[14].text,
    }


def notice_user_by_dingding(user_id, draw_num, draw_time, draw_result_list, draw_list_without_quotes, select_format):
    """
    钉钉通知用户
    :param user_id:
    :type user_id:
    :param draw_num:
    :type draw_num:
    :param draw_time:
    :type draw_time:
    :param draw_result_list:
    :type draw_result_list:
    :param draw_list_without_quotes:
    :type draw_list_without_quotes:
    :param select_format:
    :type select_format:
    :return:
    :rtype:
    """
    webhook_queryset = LotteryWebhookInfo.objects.exclude(isDeleted=True)
    headers = {
        'Content-Type': 'application/json'
    }
    hook_url_queryset = webhook_queryset.filter(createdBy=user_id)
    if not hook_url_queryset.exists():
        return 'webhook not exist'
    hook_url = hook_url_queryset.values_list('hookUrl').first()[0]
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
