# Setup Postgres docker database for project

Credit on how to setup postgres docker databae came from [Salty Crane Blog](https://www.saltycrane.com/blog/2019/01/how-run-postgresql-docker-mac-local-development/).

## Start Postgres
`$ docker-compose up -d`

## Verify Postgres is working
`$ docker logs -f my_postgres`

## Running psql
`$ docker exec -it my_postgres psql -U postgres`

## Create user name student
`$ docker exec -it my_postgres psql -U student -P student`

## Create a database
`$ docker exec -it my_postgres psql -U postgres -c "create database student"`

## Install psycopg2 module
`$ pip install -r requirements.txt`

## Run script to create, insert and query from table
`$ python query_postgres.py`

