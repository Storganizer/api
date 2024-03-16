#!/bin/bash

curl -F 'backup=@/var/home/claudio/Downloads/backup.json' http://localhost:5000/restore


# podman exec -it storganizer-postgres bash -l
# apk add postgresql-client
# psql storganizer storganizer
#
# ALTER SEQUENCE public.location_id_seq RESTART WITH 10;
# ALTER SEQUENCE public.box_id_seq RESTART WITH 92;
# ALTER SEQUENCE public.item_id_seq RESTART WITH 509;
# ALTER SEQUENCE public.person_id_seq RESTART WITH 4;
