# -- coding utf-8 --
# @Time     2021/12/4 20:14
# @Author   dicardo
# @File     local.py
# @Software PyCharm

import multiprocessing
from pathlib import Path

# from prometheus_client import multiprocess

BASE_DIR = str(Path(__file__).resolve().parent.parent.parent.parent)
bind = '127.0.0.1:5555'  # 绑定ip和端口号
backlog = 512  # 监听队列
chdir = BASE_DIR  # gunicorn要切换到的目的工作目录
timeout = 30  # 超时
worker_class = 'gthread'  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式

workers = multiprocessing.cpu_count() * 2 + 1  # 进程数
threads = 2  # 指定每个进程开启的线程数
loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误日志无法设置


# def child_exit(server, worker):
#     """针对多进程使用prometheus进行适配"""
#     multiprocess.mark_process_dead(worker.pid)
