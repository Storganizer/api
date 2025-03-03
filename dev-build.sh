#!/bin/bash

mkdir -p $(pwd)/postgres
buildah build -t storganizer-api:dev
