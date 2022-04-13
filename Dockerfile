# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR ./Docker-oc-lettings-site

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
