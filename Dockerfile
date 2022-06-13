FROM python:3.9
MAINTAINER kihyeon <kihyeon.kim@gmail.com>
#WORKDIR /home/dataprocess.api
#COPY . /home/dataprocess.api
WORKDIR /home
COPY requirements.txt /home
RUN apt-get update -y
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
