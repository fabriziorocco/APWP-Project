FROM ubuntu:latest
ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/London"
RUN apt-get -y update
RUN apt-get –y upgrade
RUN apt-get -y install cmake python3 python3-pip
RUN pip install virtualenv
WORKDIR /home
RUN python3 -m virtualenv -p python3 ./envapp
ADD . ./envapp
RUN ./envapp/bin/pip install -r ./envapp/requirements.txt