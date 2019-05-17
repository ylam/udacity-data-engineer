import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS stg_event"
staging_songs_table_drop = "DROP TABLE IF EXISTS stg_song"
songplay_table_drop = "DROP TABLE IF EXISTS fact_songplay"
user_table_drop = "DROP TABLE IF EXISTS dim_user"
song_table_drop = "DROP TABLE IF EXISTS dim_song"
artist_table_drop = "DROP TABLE IF EXISTS dim_artist"
time_table_drop = "DROP TABLE IF EXISTS dim_time"

# CREATE TABLES
staging_events_table_create= ("""
    CREATE TABLE stg_event (
        artist varchar,
        auth varchar,
        firstName varchar,
        gender varchar,
        itemInSessions int,
        lastName varchar,
        length decimal,
        level varchar,
        location varchar,
        sessionId int,
        song varchar,
        ts int,
        userAgent varchar,
        userId int,
        PRIMARY KEY (userId, sessionId, itemInSessions, ts)
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE stg_song(
        artist_id varchar,
        artist_latitude decimal,
        artist_longitude decimal,
        artist_location varchar,
        artist_name varchar,
        song_id varchar,
        title varchar,
        duration decimal,
        year int,
        PRIMARY KEY (artist_id, song_id)
    )
""")

time_table_create = ("""
    CREATE TABLE dim_time (
        start_time timestamp NOT NULL,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday int,
        PRIMARY KEY (start_time)
    )
""")

songplay_table_create = ("""
    CREATE TABLE fact_songplay (
        songplay_id int identity(0,1),
        start_time timestamp REFERENCES dim_time(start_time) NOT NULL,
        user_id int REFERENCES dim_user(user_id) NOT NULL,
        level varchar,
        song_id varchar,
        artist_id varchar,
        session_id varchar,
        location varchar,
        user_agent varchar,
        PRIMARY KEY (songplay_id)
    );
""")

user_table_create = ("""
    CREATE TABLE dim_user (
        user_id int NOT NULL,
        first_name varchar,
        last_name varchar,
        gender varchar,
        level varchar,
        PRIMARY KEY (user_id)
    )
""")

song_table_create = ("""
    CREATE TABLE dim_song (
        song_id varchar NOT NULL,
        title varchar,
        artist_id varchar,
        year int,
        duration decimal,
        PRIMARY KEY (song_id)
    )
""")

artist_table_create = ("""
    CREATE TABLE dim_artist (
        artist_id varchar NOT NULL,
        name varchar,
        location varchar,
        latitude decimal,
        longitude decimal,
        PRIMARY KEY (artist_id)
    )
""")


# STAGING TABLES
#Example
# qry = """
#     copy sporting_event_ticket from 's3://udacity-labs/tickets/split/part'
#     credentials 'aws_iam_role={}'
#     gzip delimiter ';' compupdate off region 'us-west-2';
# """.format(DWH_ROLE_ARN)

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES
# query tables from staging tables
songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
