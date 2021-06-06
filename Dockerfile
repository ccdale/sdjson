FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir poetry

COPY . .

RUN poetry install
