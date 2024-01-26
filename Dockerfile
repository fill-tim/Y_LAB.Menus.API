FROM python:3.10-slim

WORKDIR /main

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . . 

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
