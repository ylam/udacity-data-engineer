# Building a Data Pipeline with Airflow

## Requirements
* A redshift cluster credential needs to be added in connection named `redshift`. Specify the following
    * hostname
    * username
    * password
    * port
* An aws_credentials is also needed to pull data from AWS s3. Please add connection name `aws_credentials`. Specify the following
    * login as aws key
    * password as aws secret
* Redshift cluster needs to be running before running `udac_example_dag.py`

## Full pipeline

![Airflow pipeline](https://github.com/ylam/udacity-data-engineer/edit/master/Data%20Pipeline%20Airflow/airflow_datapipeline_project.png "Airflow pipeline")



