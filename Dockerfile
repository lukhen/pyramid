FROM python:3.10.2-alpine

WORKDIR /usr/src/app

RUN apk update && \
    apk add netcat-openbsd g++

RUN apk add --no-cache postgresql-dev; \
    apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    && pip install psycopg2 \
    && apk del --no-cache .build-deps

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app

RUN pip install -e .

CMD pserve development.ini --reload