# -- coding utf-8 --
# @Time     2022/11/21 11:24
# @Author   dicardo
# @File     a_task.py
# @Software PyCharm

from celery import shared_task

from celery_task.service.a_task import a_task


@shared_task
def test_task_a():
    """
    测试celery任务
    :return:
    :rtype:
    """
    a_task()
    return 'success'
