#!/bin/bash

curl -F 'backup=@/var/home/claudio/Downloads/backup.json' http://localhost:5000/restore




#ALTER SEQUENCE public.location_id_seq RESTART WITH 10;
#ALTER SEQUENCE box.location_id_seq RESTART WITH 92;
#ALTER SEQUENCE item.location_id_seq RESTART WITH 10;
