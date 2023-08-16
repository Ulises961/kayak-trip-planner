FROM python:3.10-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Thie is done because because psycopg2 would not install correclty
# when useing the "pip3 install -r requirements.txt" command
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY . /usr/src/app
COPY ./var/log/kayak-trip-planner.log /python-docker/var/log/kayak-trip-planner.log


CMD [ "python3", "/usr/src/app/Api/app.py"]
