# pull official base image
FROM python:3.10.6

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
# RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpcre3 \
    libpcre3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt
RUN pip install uwsgi

# copy project
COPY . /app