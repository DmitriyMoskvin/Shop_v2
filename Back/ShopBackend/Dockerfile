# pull official base image
FROM python:3.10.6

# set work directory
WORKDIR /app

# create folder for logs
RUN mkdir -p /app/logs && chown -R www-data:www-data /app/logs

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

# copy wait-for-it script and make it executable
COPY wait-for-it.sh /app/wait-for-it.sh

# copy project
COPY . /app

RUN chmod +x /app/wait-for-it.sh