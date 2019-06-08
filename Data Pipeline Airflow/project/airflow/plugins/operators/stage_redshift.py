from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    copy_sql_json = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT as JSON '{}'
    """
    
    copy_sql_csv = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT as CSV
    """

    @apply_defaults
    def __init__(self,
                redshift_conn_id="",
                aws_credentials_id="",
                table="",
                s3_bucket="",
                s3_key="",
                delimiter=",",
                ignore_headers=1,
                json_log_path="",
                is_json_path=1,
                create_table_query="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.delimiter = delimiter
        self.ignore_headers = ignore_headers
        self.table = table
        self.json_log_path = json_log_path
        self.is_json_path = is_json_path
        self.create_table_query = create_table_query

    def execute(self, context):
        """
            load JSON and CSV formatted files from S3 to Redshift
            SQL COPY with parameters provided
            where is s3 file
            target table
        """
        self.log.info('StageToRedshiftOperator starting')

        self.log.info(str(self.aws_credentials_id))
        aws_hook = AwsHook(self.aws_credentials_id)
        
        self.log.info(str(aws_hook))
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)

        self.log.info("Check if table exists in Redshift table")
        redshift.run(self.create_table_query)
        
        self.log.info("Clearing data from destination Redshift table")
        redshift.run("DELETE FROM {}".format(self.table))

        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)
        
        self.log.info("Using default format")
        formatted_sql = StageToRedshiftOperator.copy_sql_csv.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key
        )
        
        if self.is_json_path:
            self.log.info("Using JSON format")
            formatted_sql = StageToRedshiftOperator.copy_sql_json.format(
                self.table,
                s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.json_log_path
            )
        
        redshift.run(formatted_sql)




