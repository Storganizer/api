#!/bin/bash

podman rm -f storganizer-api
podman  run -it -d -p 5000:5000 --name storganizer-api storganizer-api:dev
