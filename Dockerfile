FROM python:3

RUN apt-get update
RUN apt-get install tzdata -y
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ="Europe/Madrid"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt .
RUN pip install -r requirements.txt
