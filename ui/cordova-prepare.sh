#!/bin/bash

rm -rf ./www
mkdir -p ./www
cp ./dist/* ./www
cp ./public/* ./www

export ANDROID_HOME=/home/claudio/Android/Sdk
#export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-11.0.18.0.10-1.fc37.x86_64
