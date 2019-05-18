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
        method varchar,
        page varchar,
        registration decimal,
        sessionId int,
        song varchar,
        status smallint,
        ts bigint,
        userAgent varchar,
        userId int,
        PRIMARY KEY (sessionId, itemInSessions, ts)
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE stg_song(
        artist_id varchar,
        artist_latitude decimal,
        artist_location varchar,
        artist_longitude decimal,
        artist_name varchar,
        duration decimal,
        num_songs int,
        song_id varchar,
        title varchar,        
        year int,
        PRIMARY KEY (song_id)
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

#Copy command documentation https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-data-source-s3.html
# STAGING TABLES
staging_events_copy = ("""
    copy stg_event from {}
    iam_role {}
    format as JSON {}
    region 'us-west-2';
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
    copy stg_song 
    from {}
    iam_role {}
    compupdate off region 'us-west-2'
    JSON 'auto' truncatecolumns;
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])

# FINAL TABLES
# query tables from staging tables
songplay_table_insert = ("""
    insert into fact_songplay(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    select TIMESTAMP 'epoch' + e.ts * INTERVAL '1 second' as start_time
        , e.userId as user_id
        , e.level as level
        , s.song_id
        , s.artist_id as artist_id
        , e.sessionId as session_id
        , e.location as location
        , e.userAgent as user_agent
    from stg_event as e
        join stg_song as s
            on e.song = s.title
            and e.firstName = s.artist_name
            and e.length = s.duration
""")

user_table_insert = ("""
    insert into dim_user(user_id, first_name, last_name, gender, level)
    select e.userId as user_id
        , e.firstName as first_name
        , e.lastName as last_name
        , e.gender as gender
        , e.level as level
    from stg_event as e
""")

song_table_insert = ("""
    insert into dim_song(song_id, title, artist_id, year, duration)
    select S.song_id as song_id
        , S.title as title
        , S.artist_id as artist_id
        , S.year as year
        , S.duration as duration
    from stg_song as S
""")

artist_table_insert = ("""
    insert into dim_artist(artist_id, name, location, latitude, longitude)
    select S.artist_id
        , S.artist_name as name
        , S.artist_location as location
        , S.artist_latitude as latitude
        , S.artist_longitude as longitude
    from stg_song as S
""")

time_table_insert = ("""
    insert into dim_time(start_time, hour, day, week, month, year, weekday)
    select data.ts
        , cast(date_part(hour, data.ts) as int) as hour
        , cast(date_part(day, data.ts) as int) as day
        , cast(date_part(week, data.ts) as int) as week
        , cast(date_part(month, data.ts) as int) as month
        , cast(date_part(year, data.ts) as int) as year
        , cast(date_part(dayofweek, data.ts) as int) as weekday
    FROM (
        SELECT TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' as ts 
        FROM stg_event
    ) as data;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
# copy_table_queries = [staging_songs_copy]
insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert, songplay_table_insert]
