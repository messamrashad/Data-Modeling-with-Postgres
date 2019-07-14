# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS SONGPLAYS;"
user_table_drop = "DROP TABLE IF EXISTS USERS;"
song_table_drop = "DROP TABLE IF EXISTS SONGS;"
artist_table_drop = "DROP TABLE IF EXISTS ARTISTS;"
time_table_drop = "DROP TABLE IF EXISTS TIME;"

# CREATE TABLES

#USER_ID, FIRST_NAME, LAST_NAME, GENDER, LEVEL
user_table_create = ("""
CREATE TABLE IF NOT EXISTS USERS (
USER_ID int NOT NULL PRIMARY KEY CONSTRAINT UNI_USER_ID UNIQUE,
FIRST_NAME varchar NOT NULL,
LAST_NAME varchar NOT NULL,
GENDER varchar NOT NULL,
LEVEL varchar NOT NULL
);
""")

#SONG_ID, TITLE, ARTIST_ID, YEAR, DURATION
song_table_create = ("""
CREATE TABLE IF NOT EXISTS SONGS (
SONG_ID varchar NOT NULL PRIMARY KEY,
TITLE varchar NOT NULL, 
ARTIST_ID varchar NOT NULL,
YEAR int NOT NULL,
DURATION FLOAT NOT NULL
);
""")

#ARTIST_ID, NAME, LOCATION, LATITUDE, LONGITUDE
artist_table_create = ("""
CREATE TABLE IF NOT EXISTS ARTISTS (
ARTIST_ID varchar NOT NULL PRIMARY KEY CONSTRAINT UNI_ARTIST_ID UNIQUE,
NAME varchar NOT NULL, 
LOCATION varchar NOT NULL,
LATITUDE NUMERIC NOT NULL,
LONGITUDE NUMERIC NOT NULL
);
""")

#START_TIME, HOUR, DAY, WEEK, MONTH, YEAR, WEEKDAY
time_table_create = ("""
CREATE TABLE IF NOT EXISTS TIME (
START_TIME TIME NOT NULL PRIMARY KEY CONSTRAINT UNI_START_TIME UNIQUE, 
HOUR int NOT NULL,
DAY int NOT NULL,
WEEK int NOT NULL,
MONTH int NOT NULL,
YEAR int NOT NULL,
WEEKDAY int NOT NULL
);
""")

#SONGPLAY_ID, START_TIME, USER_ID, LEVEL, SONG_ID, ARTIST_ID, SESSION_ID, LOCATION, USER_AGENT
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS SONGPLAYS (
SONGPLAY_ID SERIAL PRIMARY KEY,
START_TIME TIME NOT NULL,
USER_ID int NOT NULL,
LEVEL varchar NOT NULL,
SONG_ID varchar,
ARTIST_ID varchar,
SESSION_ID int NOT NULL, 
LOCATION varchar NOT NULL,
USER_AGENT varchar NOT NULL,
FOREIGN KEY (USER_ID) REFERENCES USERS (USER_ID),
FOREIGN KEY (ARTIST_ID) REFERENCES ARTISTS (ARTIST_ID),
FOREIGN KEY (SONG_ID) REFERENCES SONGS (SONG_ID)
);
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO SONGPLAYS (SONG_ID, ARTIST_ID, START_TIME, USER_ID, LEVEL, SESSION_ID, LOCATION, USER_AGENT) \
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""")

user_table_insert = ("""INSERT INTO USERS (USER_ID, FIRST_NAME, LAST_NAME, GENDER, LEVEL) \
                      VALUES (%s,%s,%s,%s,%s) \
                      ON CONFLICT ON CONSTRAINT UNI_USER_ID DO UPDATE SET LEVEL = excluded.LEVEL;""")

song_table_insert = ("""INSERT INTO SONGS (SONG_ID, TITLE, ARTIST_ID, YEAR, DURATION) \
                      VALUES (%s,%s,%s,%s,%s) \
                      ON CONFLICT (SONG_ID) DO NOTHING;""")

artist_table_insert = ("""INSERT INTO ARTISTS (ARTIST_ID, NAME, LOCATION, LATITUDE, LONGITUDE) \
                      VALUES (%s,%s,%s,%s,%s) \
                      ON CONFLICT ON CONSTRAINT UNI_ARTIST_ID DO NOTHING""")


time_table_insert = ("""INSERT INTO TIME (START_TIME, HOUR, DAY, WEEK, MONTH, YEAR, WEEKDAY) \
                      VALUES (%s,%s,%s,%s,%s,%s,%s) \
                      ON CONFLICT ON CONSTRAINT UNI_START_TIME DO NOTHING;""")

# FIND SONGS

song_select = ("SELECT s.SONG_ID, a.ARTIST_ID FROM SONGS s JOIN ARTISTS a ON s.ARTIST_ID = a.ARTIST_ID \
                WHERE s.TITLE = %s AND a.NAME = %s AND s.duration = %s")

# QUERY LISTS
##Change the order of the queries in "create_table_queries" due to building the proper PK/FK constraints.
create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
