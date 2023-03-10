FROM python:3.10.6-slim-buster as base
WORKDIR /app

ENV PYTHONUNBUFFERED=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get -y install gcc libpq-dev python-dev nano && \
    pip3 install --upgrade pip

ADD .env  .

FROM base as api

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./api /app/api
COPY ./api-data /app/data


FROM base as backup

RUN apt-get update && \
    apt-get install -y cron && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./api /app/api

COPY crontab /opt/hello/backup.cronjob
RUN chmod 0644 /opt/hello/backup.cronjob && \
	crontab /opt/hello/backup.cronjob
RUN touch /var/log/cron.log
CMD (cron -f &) && tail -f /var/log/cron.log