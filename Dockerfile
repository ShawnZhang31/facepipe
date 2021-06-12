FROM python:3.7

ENV FLASK_APP cmit_facepipe.py
ENV FLASK_CONFIG production

RUN apt-get update -y
RUN apt-get install cmake -y

#opencv的依赖包
RUN apt-get install python3-opencv -y

WORKDIR /cmit_facepipe

COPY . .


# 时区设置
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo 'Asia/Shanghai' >/etc/timezone


RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

RUN ["chmod", "+x", "./boot.sh"]
# 运行配置
EXPOSE 5000
ENTRYPOINT ["sh", "./boot.sh" ]