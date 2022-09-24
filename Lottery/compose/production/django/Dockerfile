FROM registry.cn-hangzhou.aliyuncs.com/dicardo/python-django:v1.0.0

RUN mkdir app
COPY . app
WORKDIR /root/app/Lottery
RUN pip install -r app/Lottery/requirements/base.txt
CMD sh /app/Lottery/compose/production/django/start && tail -f -n 100 /app/Lottery/logs/nohup.out