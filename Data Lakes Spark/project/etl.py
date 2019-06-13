import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Using data from song I generate the following tables 
    songs
    artist
    """
    # get filepath to song data file
    song_data = os.path.join(input_data, "song_data/A/*/*/*.json")
    
    # song_data = os.path.join(input_data, "song_data/A/A/A/TRAAAAK128F9318786.json")
    output_songs_table = os.path.join(output_data, "songs_table")
    output_artists_table = os.path.join(output_data, "artists_table")
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select('song_id', 'title', 'artist_id', 'year', 'duration').dropDuplicates()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.parquet(output_songs_table, mode='overwrite')   

    # extract columns to create artists table
    artists_table = df.select('artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude').dropDuplicates()
    
    # write artists table to parquet files
    artists_table.write.parquet(output_artists_table, mode='overwrite')   


def process_log_data(spark, input_data, output_data):
    """
    Using data from log and song plays I generate the following tables 
    users
    time
    songplays
    """
    # get filepath to log data file
    log_data = os.path.join(input_data, "log-data/2018/11/*.json")
    song_data = os.path.join(input_data, "song_data/A/*/*/*.json")
    
    # log_data = os.path.join(input_data, "log-data/2018/11/2018-11-01-events.json")
    # song_data = os.path.join(input_data, "song_data/A/A/A/TRAAAAK128F9318786.json")
    
    output_users_table = os.path.join(output_data, "users_table")
    output_time_table = os.path.join(output_data, "time_table")
    output_songplays_table = os.path.join(output_data, "songplays_table")
    
    # read log data file
    df = spark.read.json(log_data)
    
    # print(df.printSchema())
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong').dropDuplicates()

    # extract columns for users table    
    users_table = df.select('userId', 'firstName', 'lastName', 'gender', 'level').dropDuplicates()
    
    # write users table to parquet files
    users_table.write.parquet(output_users_table, mode='overwrite')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: str(int(int(x) / 1000)))
    df = df.withColumn("timestamp", get_timestamp(df.ts))
    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000.0)))
    df = df.withColumn("datetime", get_datetime(df.ts))
    
    # extract columns to create time table
    time_table = df.select(
        'timestamp',
        hour('datetime').alias('hour'),
        dayofmonth('datetime').alias('day'),
        weekofyear('datetime').alias('week'),
        month('datetime').alias('month'),
        year('datetime').alias('year'),
        date_format('datetime', 'F').alias('weekday')
    )
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy('year', 'month').parquet('output_time_table')

    # read in song data to use for songplays table
    song_df = spark.read.json(song_data)
    
    # create temporary views
    song_df.createOrReplaceTempView('song_data')
    df.createOrReplaceTempView('log_data')

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql("""
        select s.song_id
            , l.userId
            , l.level
            , l.artist
            , l.sessionId
            , l.location
            , l.userAgent
            , l.timestamp
            , month('datetime') as month
            , year('datetime') as year
        from song_data as s
            join log_data as l
                on s.title = l.song
                and s.artist_name = l.artist
                and s.duration = l.length
    """)

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy('year', 'month').parquet(output_songplays_table)


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://dend-ylam-bucket/data-lake/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
