# -- coding utf-8 --
# @Time     2022/5/8 下午10:59
# @Author   dicardo
# @File     lottery_view.py
# @Software PyCharm

from typing import Any

import django_filters.rest_framework
from rest_framework import generics, viewsets, filters
from rest_framework.request import Request
from rest_framework.response import Response

from common.api_rest_response import ApiRestResponse, ResponseEnum
from lottery.models import LotterySelectInfo
from lottery.serializers.lottery_serializer import LotterySerializer


class MyLotteryView(generics.ListCreateAPIView, viewsets.GenericViewSet):
    """
    个人lottery号码管理
    """
    queryset = LotterySelectInfo.objects.exclude(isDeleted=True)
    serializer_class = LotterySerializer
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=ApiRestResponse().response(enum=ResponseEnum.SUCCESS))
