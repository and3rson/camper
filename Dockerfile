FROM python:3.6.3-jessie
MAINTAINER Andrew Dunai

ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

# Install add-apt-repository & wget (required to build this image)
RUN \
    apt-get update
RUN \
    apt-get install --assume-yes \
    software-properties-common wget

RUN mkdir /root/camper
WORKDIR /root/camper

COPY ./requirements.txt /root/camper

RUN \
    pip install -r ./requirements.txt

RUN \
    apt-get install --assume-yes \
    netcat
COPY ./manage.py /root/camper
COPY ./camper /root/camper/camper
COPY ./bin /root/camper/bin

RUN pwd
RUN ls -l

EXPOSE 9090

