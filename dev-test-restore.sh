#!/bin/bash

curl -F 'backup=@/var/home/claudio/Downloads/backup.json' http://localhost:5000/restore
