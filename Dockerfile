FROM python:3.10.6-slim-buster as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get -y install gcc libpq-dev python-dev && \
    pip3 install --upgrade pip

WORKDIR /app

FROM base as api
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./api api
COPY ./data api/data
COPY ./.env api/.env
