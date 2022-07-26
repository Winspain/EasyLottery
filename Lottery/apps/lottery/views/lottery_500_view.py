# -- coding utf-8 --
# @Time     2022/10/2 20:06
# @Author   dicardo
# @File     lottery_500_view.py
# @Software PyCharm

from typing import Any

import django_filters.rest_framework
from rest_framework import generics, viewsets, filters
from rest_framework.request import Request
from rest_framework.response import Response

from common.api_rest_response import ApiRestResponse, ResponseEnum
from lottery.models import LotteryInfo
from lottery.serializers.lottery_serializer import Lottery500Serializer
from lottery.service.get_lottery import get_latest_number_by_500
from lottery.service.permission import CeleryPermission


class Lottery500View(generics.ListCreateAPIView, viewsets.GenericViewSet):
    """
    500网爬取号码
    """
    queryset = LotteryInfo.objects.exclude(isDeleted=True)
    serializer_class = Lottery500Serializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    permission_classes = [CeleryPermission]

    def create(self, request: Request, *args: Any, **kwargs: Any) -> object:
        """
        爬取号码存入数据库
        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        latest_number = get_latest_number_by_500()
        if not latest_number:
            return Response(data=ApiRestResponse().response(enum=ResponseEnum.FAIL_SPIDER_500))
        serializer = self.get_serializer(data=latest_number)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=ApiRestResponse().response(enum=ResponseEnum.SUCCESS))
