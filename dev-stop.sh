#!/bin/bash

podman rm -f storganizer-api
podman rm -f storganizer-postgres
podman pod rm storganizer
