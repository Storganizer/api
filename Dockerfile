from docker.io/python:3.12-slim

RUN apt update -y && apt purge gcc && apt install -y libpq-dev rustc g++; \
	mkdir /app

COPY /controller /app/controller
COPY /model /app/model
COPY /api.py /app/api.py
COPY /requirements.txt /app/requirements.txt

WORKDIR  /app

RUN python -m pip install --upgrade pip \
    && pip install --user -r /app/requirements.txt

EXPOSE 5000

ENTRYPOINT ["/app/api.py"]
