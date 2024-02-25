#!/bin/bash

podman rm -f storganizer-api
podman rm -f storganizer-postgres
podman pod rm storganizer



podman pod create --name storganizer -p 5000:5000

podman  run -it -d\
  --pod=storganizer \
  -e SQLALCHEMY_CONNECTION_STRING='postgresql+psycopg2://storganizer@localhost/storganizer' \
  -e FLASK_ENV='development' \
  -v /var/home/claudio/Development/storganizer/api:/app:z \
  --name storganizer-api storganizer-api:dev

podman run -it -d\
  --pod=storganizer \
  --name storganizer-postgres \
  -e POSTGRES_DB=storganizer \
  -e POSTGRES_USER=storganizer \
  -e POSTGRES_PASSWORD=storganizer \
  -v /var/home/claudio/podman/storganizer-api/postgres/:/var/lib/postgresql/data:z \
  docker.io/postgres:16-alpine