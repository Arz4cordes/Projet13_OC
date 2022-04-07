# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR ./Docker-oc-lettings-site

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY lettings lettings
COPY profiles profiles
COPY oc_lettings_site oc_lettings_site

CMD [ "python3", "-m" , "django", "manage.py", "--host=0.0.0.0"]
