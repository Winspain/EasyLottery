FROM registry.cn-hangzhou.aliyuncs.com/dicardo/python-django:v1.0.0
#FROM python:3.8-slim-buster

RUN mkdir app
COPY . app
RUN pip install -r app/requirements/base.txt
CMD sh app/compose/local/django/start && tail -f -n 100 app/nohup.out