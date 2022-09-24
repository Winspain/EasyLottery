# -- coding utf-8 --
# @Time     2021/6/27 21:55
# @Author   dicardo
# @File     custom_exception.py
# @Software PyCharm

from rest_framework.views import exception_handler

"""自定义异常实现"""


def custom_exception_handler(exc, context):
    try:
        response = exception_handler(exc, context)
        error = exc.get_codes()
        error_dict = {key: value[0] for key, value in error.items()}
        if response is not None:
            response.data.clear()
            response.data = error_dict

        return response
    except Exception as e:
        return response
