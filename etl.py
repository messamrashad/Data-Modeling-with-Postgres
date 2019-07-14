import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This procedure processes a song file whose filepath has been provided as an arugment with an opening cursor on the DB.
    It extracts the song and artist information in order to store it into SONGS and ARTISTS Tables.
    
    INPUTS: 
    * cur: the cursor variable
    * filepath: the file path to the song file
    """
    ##Open song_data files
    df = pd.read_json(filepath, lines = True) 

    ##Insert song information into SONGS Table
    song_data = list(df[['song_id','title','artist_id','year','duration']].loc[:].values[0])
    cur.execute(song_table_insert, song_data)
    
    ##Insert artist information into ARTISTS Table
    artist_data = list(df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].loc[:].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This procedure processes a log file whose filepath has been provided as an arugment with an opening cursor on the DB.
    It extracts the log rows information in order to store it into USERS and SONGPLAYS Tables.
    Some modifications will be needed before storing the values into their tables. For exmaple, converting "ts" column to datetime datatype.
    
    INPUTS: 
    * cur: the cursor variable
    * filepath: the file path to the song file
    """
    ##Open log_data files
    df = pd.read_json(filepath, lines= True)

    ##Filter records with "NextSong" Page.
    df = df.query("page =='NextSong'")

    ##Convert "ts" column in the DataFrame to datetime datatype
    t = pd.to_datetime(df['ts'], unit='ms')
    pd.set_option('mode.chained_assignment', None)
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    ##Creating new DataFrame contains the splits of the provided timestamps
    time_data = (t.dt.time,t.dt.hour,t.dt.day,t.dt.week,t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('Start_Time','Hour', 'Day', 'WeekofYear', 'Month', 'Year', 'WeekDay')
    time_df = pd.DataFrame(dict(zip(column_labels,time_data)), columns = column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    ##Get data for USERS Table
    user_df = df[['userId','firstName','lastName','gender','level']].loc[:]

    ##Insert USERS data into USERS Table
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    ##Get/Insert songplay data into SONGPLAY Table
    for index, row in df.iterrows():
        
        ##Get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        ##Insert songplay record into SONGPLAY Table
        songplay_data = (songid, artistid, row['ts'],row['userId'],row['level'],row['sessionId'],row['location'],row['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)
        

def process_data(cur, conn, filepath, func):
    """
    This procedure gets all files in the provided filepath and send each file to the provided function to be processed and loaded into specified tables.
    This function called within the main procedure with the below input arguments:
    
    INPUTS: 
    * cur: the cursor variable.
    * conn: A connection to DB.
    * filepath: the file path to the song file.
    * func: Name of the function to pass arguments to.
    """
    ##Get all files matching extension from directory
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
    """
    This Main procedure create connection to DB Sparkifydb, and open the cursor. Finally, it calls the process_data procedure with the specified arguments.
    
    INPUTS: 
    No Inputs for this proceudre.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
