FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
  && apt-get -y install libpq-dev gcc \
  && rm -rf /var/lib/apt/lists/*

COPY src src
COPY Makefile Makefile
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENV PYTHONPATH=src
ENV FLASK_APP=app:app

EXPOSE 9000

CMD flask run --host 0.0.0.0 --port 9000 --debug
