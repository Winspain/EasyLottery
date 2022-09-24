# -- coding utf-8 --
# @Time     2021/6/27 21:38
# @Author   dicardo
# @File     __init__.py.py
# @Software PyCharm

from easy_lottery.config.celery.local import app as celery_app

__all__ = ("celery_app",)
