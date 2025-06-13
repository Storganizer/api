from docker.io/python:3.12-slim

ENV SQLALCHEMY_CONNECTION_STRING 'sqlite+pysqlite:///storganizer.db'

RUN apt update -y && apt purge gcc && apt --no-install-recommends install -y libpq-dev rustc g++; \
	mkdir /app

#COPY /controller /app/controller
#COPY /model /app/model
#COPY /api.py /app/api.py
#COPY /seed.py /app/seed.py
COPY /requirements.txt /app/requirements.txt

WORKDIR  /app

RUN python -m pip install --upgrade pip \
    && pip install --user -r /app/requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "/app/api.py"]
