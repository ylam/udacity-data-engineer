FROM puckel/docker-airflow
LABEL maintainer="yplam@ca.ibm.com"

RUN pip install --user --no-cache-dir boto3
RUN pip install --user --no-cache-dir psycopg2-binary
ENV AIRFLOW_HOME=/usr/local/airflow
COPY /config/airflow.cfg /usr/local/airflow/airflow.cfg
COPY /airflow/dags /usr/local/airflow/dags
COPY /airflow/plugins /usr/local/airflow/plugins
COPY /script/entrypoint.sh /entrypoint.sh
COPY requirements.txt /