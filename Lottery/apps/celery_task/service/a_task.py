# -- coding utf-8 --
# @Time     2022/11/21 15:44
# @Author   dicardo
# @File     a_task.py
# @Software PyCharm

from common.constant.log_const import DJANGO_LOGGER
from lottery.models import LotteryInfo


def a_task():
    lottery_queryset = LotteryInfo.objects.exclude(isDeleted=True)
    DJANGO_LOGGER.warning(lottery_queryset)
