FROM registry.cn-hangzhou.aliyuncs.com/dicardo/python-django:v1.0.0

RUN mkdir app
COPY . app
RUN pip install -r app/Lottery/requirements/base.txt
CMD sh /app/Lottery/compose/production/django/start && tail -f -n 100 /app/Lottery/compose/production/django/nohup.out