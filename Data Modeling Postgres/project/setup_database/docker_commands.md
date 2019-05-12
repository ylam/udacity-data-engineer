# Setup Postgres docker database for project

Credit on how to setup postgres docker databae came from [Salty Crane Blog](https://www.saltycrane.com/blog/2019/01/how-run-postgresql-docker-mac-local-development/).

## Start Postgres
`$ docker-compose up -d`

## Verify Postgres is working
`$ docker logs -f my_postgres`

## Running psql
`$ docker exec -it my_postgres psql -U postgres`

## Create a database
`postgres=# Create database studentdb;`

## Create user name student
`postgres=# CREATE USER student with encrypted password 'student';`

## Grant user to create database
`postgres=# ALTER USER student CREATEDB;`

## Install psycopg2 module
`$ pip install -r requirements.txt`

## Run script to create, insert and query from table
`$ python query_postgres.py`

