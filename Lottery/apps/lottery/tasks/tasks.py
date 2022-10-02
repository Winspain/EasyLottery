# -- coding utf-8 --
# @Time     2022/10/2 23:46
# @Author   dicardo
# @File     tasks.py
# @Software PyCharm

from easy_lottery.config.celery.production import app


@app.shared_task
def add(x, y):
    return x + y
