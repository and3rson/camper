FROM node
MAINTAINER Andrew Dunai

ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /root/camper
WORKDIR /root/camper
COPY package.json /root/camper

RUN npm i

#RUN mkdir /root/camper/dist
COPY Gulpfile.js /root/camper
COPY ./src /root/camper/src
COPY ./static /root/camper/static
COPY ./views /root/camper/views

#RUN ls -l
#RUN ls -l dist

RUN npm run build

EXPOSE 9091

