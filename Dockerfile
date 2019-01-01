FROM python:3.6
MAINTAINER alpy

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -qq -y build-essential libffi-dev python3-dev
RUN apt-get install -y poppler-utils

EXPOSE 5000
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./app/app.py"]
