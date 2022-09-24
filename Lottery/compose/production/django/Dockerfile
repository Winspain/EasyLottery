FROM registry.cn-hangzhou.aliyuncs.com/dicardo/python-django:v1.0.0

RUN mkdir app
COPY . app
WORKDIR /root/app/Lottery
RUN pip install -r requirements/base.txt
ENTRYPOINT ["/bin/sh","-c","sh compose/production/django/start && tail -f -n 100 logs/nohup.out"]