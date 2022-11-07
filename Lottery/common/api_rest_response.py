# -- coding utf-8 --
# @Time     2021/7/3 14:24
# @Author   dicardo
# @File     api_rest_response.py
# @Software PyCharm

from enum import Enum
from enum import unique


class ApiRestResponse:

    @staticmethod
    def response(enum, message='', content=''):
        """
        HTTP请求统一返回格式
        """
        # 和web交互的信息使用驼峰命名,异常枚举是内部使用,因此采用Python推荐的蛇形命名法
        response_body = {
            'errorCode': enum.value['error_code'],
            'message': enum.value['message'] if not message else message,
            'data': content,
        }
        return response_body


@unique
class ResponseEnum(Enum):
    """
    00 微服务 00 模块 00 编号
    """
    SUCCESS = {'error_code': '000000', 'message': 'SUCCESS'}
    EXAMPLE_ENUM = {'error_code': '010001', 'message': 'ok'}
    FAIL_SPIDER_500 = {'error_code': '010101', 'message': '500网抓取失败'}
