FROM python:3.6-alpine3.7

MAINTAINER docker_user python-dog@gmail.com

ENV LANG C.UTF-8

COPY repositories /etc/apk

RUN apk add --update --no-cache \
    mariadb-dev \
	gcc \
	libffi-dev \
    musl-dev \
	supervisor \
	tzdata \
	linux-headers \
	freetype-dev \
	libxml2-dev \
	libxslt-dev

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

WORKDIR src/

COPY requirements.txt .

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

ENV PYTHONPATH=/src/yuehu:/src/yuehu/apps

RUN mkdir /etc/supervisor.d/
