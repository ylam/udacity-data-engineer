Data Pipeline with Airflow

Run `/opt/airflow/start.sh` to start Airflow webserver.

Run schedule in airflow
    datetime.datetime.now() - datetime.timedelta(days=60)
    schedule_interval = "@monthly"

airflow can backfill

Airflow comes with many Operators that can perform common operations

PythonOperator
PostgresOperator
RedshiftToS3Operator
BashOperator
Sensor

Nodes = Tasks
Edges = Ordering and dependencies between tasks

a >> b means a comes before b
a << b means a comes after b