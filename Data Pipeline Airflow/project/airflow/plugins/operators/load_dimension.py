from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    dimensions_sql_template = """
        DROP TABLE IF EXISTS {destination_table};
        CREATE TABLE {destination_table} AS 
        {sql_query};
    """
    
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 destination_table='',
                 sql_query='',
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.destination_table = destination_table
        self.sql_query = sql_query

    def execute(self, context):
        self.log.info('LoadDimensionOperator running')
        self.log.info(self.destination_table)
        self.log.info(self.sql_query)
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        dimension_sql = LoadDimensionOperator.dimensions_sql_template.format(
            destination_table = self.destination_table,
            sql_query = self.sql_query
        )
        
        redshift.run(dimension_sql)
