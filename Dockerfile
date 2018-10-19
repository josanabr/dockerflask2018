FROM ubuntu

MAINTAINER John Sanabria - john.sanabria@gmail.com

RUN apt-get update

RUN apt-get -y --fix-missing install python3-pip ; exit 0

RUN pip3 install Flask

EXPOSE 5000
