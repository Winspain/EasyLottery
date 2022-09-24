# -- coding utf-8 --
# @Time     2021/7/3 14:32
# @Author   dicardo
# @File     api_logging_middleware.py
# @Software PyCharm

from __future__ import unicode_literals

import json
import logging
import time


class ApiLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_logger = logging.getLogger('api')

    def __call__(self, request):
        request.start_time = time.time()
        try:
            body = json.loads(request.body)
        except Exception:
            body = str(request.body)

        if request.FILES:
            body = 'body内容为文件'

        post = str(request.POST)

        response = self.get_response(request)
        execute_time = round((time.time() - request.start_time) * 1000)

        try:
            response_data = str(response.content, encoding='utf-8') if response.status_code != 500 else 'Please check error.log'
        except Exception as e:
            response_data = e

        extra = {
            'user': request.user.username if request.user.id else 'AnonymousUser',
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'response_time': execute_time,
            'response_body': response_data

        }

        if request.path in EXCLUDE_PATH:
            self.api_logger.info(f'{request.user} {execute_time}ms {request.method} {request.path} {body} {post} {response.status_code} {response.reason_phrase}', extra=extra)

        elif request.method != 'GET':
            self.api_logger.info(f'{request.user} {execute_time}ms {request.method} {request.path} {body} {post} {response.status_code} {response.reason_phrase} {response_data}', extra=extra)

        else:
            self.api_logger.info(f'{request.user} {execute_time}ms {request.method} {request.path} {response.status_code} {response.reason_phrase}', extra=extra)
        return response


EXCLUDE_PATH = [
    '/metrics',
]
