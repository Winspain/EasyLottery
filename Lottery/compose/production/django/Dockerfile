FROM registry.cn-hangzhou.aliyuncs.com/dicardo/python-django:v1.0.0

COPY . /root/app
RUN chmod -R 777 /root/app
WORKDIR /root/app/Lottery
RUN pip install --upgrade pip
RUN pip install -r requirements/production.txt
ENTRYPOINT ["/bin/sh","-c","sh compose/production/django/start && tail -f -n 100 logs/nohup.out"]
