FROM python:3.7-stretch
ENV PYTHONUNBUFFERED 1

RUN mkdir /shuup-packages
RUN mkdir /app
WORKDIR /app

# We really should just make an image that we pull from somewhere
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get update && apt-get install -y \
    mysql-client \
    nodejs
COPY wheels /app/wheels/
RUN pip install prequ
RUN pip install mysqlclient
RUN pip install psycopg2

COPY . /app/
