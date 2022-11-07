# -- coding utf-8 --
# @Time     2022/5/8 下午10:59
# @Author   dicardo
# @File     lottery_view.py
# @Software PyCharm
import json
from typing import Any

import django_filters.rest_framework
import requests
from rest_framework import generics, viewsets, filters
from rest_framework.request import Request
from rest_framework.response import Response

from common.api_rest_response import ApiRestResponse, ResponseEnum
from lottery.models import LotterySelectInfo, LotteryInfo, LotteryWebhookInfo
from lottery.serializers.lottery_serializer import LotterySelectSerializer
from lottery.service.lottery_rules import lottery_compare, lottery_rule
from lottery.service.permission import CeleryPermission


class MyLotteryView(generics.ListCreateAPIView, viewsets.GenericViewSet):
    """
    个人lottery号码管理
    """
    queryset = LotterySelectInfo.objects.exclude(isDeleted=True)
    serializer_class = LotterySelectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> object:
        """
        查询个人lottery号码
        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(data=ApiRestResponse().response(enum=ResponseEnum.SUCCESS, content=serializer.data))

    def create(self, request: Request, *args: Any, **kwargs: Any) -> object:
        """
        新增个人lottery号码
        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        user_id = request.user.id
        request_data = request.data
        request_data['createdBy'] = user_id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=ApiRestResponse().response(enum=ResponseEnum.SUCCESS))


class MyLotteryCompareView(generics.ListAPIView, viewsets.GenericViewSet):
    lottery_queryset = LotteryInfo.objects.exclude(isDeleted=True)
    select_queryset = LotterySelectInfo.objects.exclude(isDeleted=True)
    webhook_queryset = LotteryWebhookInfo.objects.exclude(isDeleted=True)
    permission_classes = [CeleryPermission]

    def list(self, request: Request, *args: Any, **kwargs: Any) -> object:
        """
        个人lottery开奖情况
        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        draw_info = self.lottery_queryset.latest('drawTime')
        draw_num = draw_info.drawNum
        draw_time = draw_info.drawTime
        draw_list = [draw_info.frontNum1, draw_info.frontNum2, draw_info.frontNum3, draw_info.frontNum4, draw_info.frontNum5, draw_info.backNum1, draw_info.backNum2]
        draw_list_without_quotes = str(draw_list).replace("'", ' ')  # 格式和自选号码保持一致,填充空格
        # TODO 后续根据用户分别筛选
        select_info = self.select_queryset.filter(createdBy='1')
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
        hook_url = self.webhook_queryset.filter(createdBy='1').values_list('hookUrl').first()[0]
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
        return Response(data=ApiRestResponse().response(enum=ResponseEnum.SUCCESS, content=draw_result_list))
