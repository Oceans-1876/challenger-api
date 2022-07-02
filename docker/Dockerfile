FROM python:3.10-slim

ARG WORKERS
ENV WORKERS=${WORKERS:-4}

ENV POETRY_VIRTUALENVS_CREATE false

RUN apt update && apt upgrade -y

WORKDIR /usr/src/challenger-api

COPY . .

RUN pip install -U pip
RUN pip install poetry
RUN poetry install

CMD gunicorn -b 0.0.0.0:8000 -w ${WORKERS} -k uvicorn.workers.UvicornWorker app.main:app
