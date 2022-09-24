from django.shortcuts import render

# Create your views here.

from typing import Any

from rest_framework import generics, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users import tasks
from common.api_rest_response import ApiRestResponse, ResponseEnum


class ExampleView(generics.ListAPIView, viewsets.GenericViewSet):
    """
    example
    """
    permission_classes = ()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> object:
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # res = tasks.add.delay(1, 3)
        return Response(data=ApiRestResponse().response(enum=ResponseEnum.SUCCESS))
