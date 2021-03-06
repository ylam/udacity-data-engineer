import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Extract from song data and insert into songs and artists tables

    Parameters:
    cur is the cursor for database
    filepath is the song data file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e: 
        print("Error: Could not insert song record to Postgres database")
        print(e)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    try:
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as e: 
        print("Error: Could not insert artist record to Postgres database")
        print(e)


def process_log_file(cur, filepath):
    """Extract from user log data and insert into time and users tables

    Parameters:
    cur is the cursor for database
    filepath is the log data file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong'].reset_index()

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour.values, t.dt.day.values, t.dt.weekofyear.values, t.dt.month.values, t.dt.year.values, t.dt.weekday.values)
    column_labels = ('start_time', 'hour', 'day', 'weekOfyear', 'month', 'year', 'weekday')
    my_dict = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame.from_dict(my_dict)
    time_df.head()

    #Used by time dimension
    df['start_time'] = t

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e: 
            print("Error: Could not insert time record to Postgres database")
            print(e)

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as e: 
            print("Error: Could not insert user record to Postgres database")
            print(e)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

        # insert songplay record
        songplay_data = (str(row.start_time), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except psycopg2.Error as e: 
            print("Error: Could not insert songplay record to Postgres database")
            print(e)


def process_data(cur, conn, filepath, func):
    """Collect all the log and song data for extract and load

    Parameters:
    cur is the cursor for database
    conn is the connection to database
    filepath is the path to the data files
    func is the name of function to call
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student port=5432")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()