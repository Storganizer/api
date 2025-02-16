#!/bin/bash

podman rm -f storganizer-api
podman rm -f storganizer-postgres
podman pod rm storganizer

podman pod create --name storganizer -p 5000:5000 -p 5432:5432

podman  run -it -d\
  --pod=storganizer \
  -e SQLALCHEMY_CONNECTION_STRING='postgresql+psycopg2://storganizer@localhost/storganizer' \
  -v $(pwd)/:/app:z \
  --name storganizer-api storganizer-api:dev

podman run -it -d\
  --pod=storganizer \
  --name storganizer-postgres \
  -e POSTGRES_DB=storganizer \
  -e POSTGRES_USER=storganizer \
  -e POSTGRES_PASSWORD=storganizer \
  -v $(pwd)/postgres/:/var/lib/postgresql/data:z \
  docker.io/postgres:16-alpine