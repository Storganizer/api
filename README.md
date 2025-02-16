# README - ToDo


1. If you start the api for the first time, install all needed packages and create an empty folder for postgres.

```
	pip install -r requirements.txt
	mkdir -p $(pwd)/postgres

```


2. Build the dev container

```
	./dev-build.sh

```


2. Start the containers

```
	./dev-start.sh

```

2.1. If you start the database for the first time, create the tables.

```
	podman exec -it storganizer-api ./db-create.py

```


3. Stop and remove the containers

```
	./dev-stop.sh

```