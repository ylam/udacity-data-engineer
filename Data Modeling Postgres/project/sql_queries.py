# DROP TABLES

songplay_table_drop = "DROP table IF EXISTS songplays"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS songs"
artist_table_drop = "DROP table IF EXISTS artists"
time_table_drop = "DROP table IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id serial, 
        start_time timestamp, 
        user_id int NOT NULL, 
        level varchar, 
        song_id int, 
        artist_id int, 
        session_id int, 
        location varchar, 
        user_agent varchar,
        PRIMARY KEY (songplay_id)        
        );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id int NOT NULL,
        first_name varchar,
        last_name varchar,
        gender varchar,
        level varchar,
        PRIMARY KEY (user_id)
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id varchar NOT NULL,
        title varchar,
        artist_id varchar,
        year int,
        duration decimal,
        PRIMARY KEY (song_id)
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id varchar NOT NULL,
        name varchar,
        location varchar,
        latitude decimal,
        longitude decimal,
        PRIMARY KEY (artist_id)
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time timestamp NOT NULL,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday int,
        PRIMARY KEY (start_time)
    );
""")

# INSERT RECORDS

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

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]