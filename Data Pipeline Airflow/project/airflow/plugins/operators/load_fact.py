from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    fact_sql_template = """
        DROP TABLE IF EXISTS {destination_table};
        CREATE TABLE {destination_table} AS 
        {sql_query}
    """
    
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 destination_table='',
                 sql_query='',
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.destination_table = destination_table
        self.sql_query = sql_query

    def execute(self, context):
        self.log.info('LoadFactOperator not implemented yet')
        
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)
        fact_sql = LoadFactOperator.fact_sql_template.format(
            destination_table = self.destination_table,
            sql_query = self.sql_query
        )
        
        redshift.run(fact_sql)
