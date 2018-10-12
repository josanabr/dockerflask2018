FROM ubuntu
RUN apt-get update && apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip3 install Flask
EXPOSE 5000
