# Data Modeling Cassandra Project

Sparkify has event data which we want to query about. Since it has a lot of data we choose to import the data into Cassandra database. Business analysts have provided us some information that we like which helps us build our data model.

## Setup Cassandra locally
I setup a local running Apache Cassandra using their docker image. Details on how to run it is found in folder (setup_cassandra)[https://github.com/ylam/udacity-data-engineer/tree/master/Data%20Modeling%20Cassandra/setup_cassandra].

## Process data
The work of data extract, load and query is found in a jupyter notebook named project_cassandra.ipynb. 