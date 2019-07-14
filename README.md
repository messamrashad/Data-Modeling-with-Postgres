# Data Modeling with Postgres
In this project, I will apply data modeling techniques with Postgres and build an ETL pipeline using Python. To complete the project, I will need to define fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these tables in Postgres using Python and SQL.

## Summary:

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.


## Purpose:

The purpose of this project is to build an ETL pipeline for a database hosted on Redshift. I choose to implement DB with STAR schema consists of one fact table (SongPlays) and many dimension tables (USERS, ARTISTS, SONGS, TIME).
**This DB with such an organized schema will help the start-up Sparkify to have a DB with high scalability and very useful for analytical purposes**. The Analytics Team of sparkify with using of simple queries can extract many insights about **songs, users' behaviour, and most important for marketing campings, are the songs users are listening to**.

#### As a Data engineer, I was more interested in building an ETL pipeline for a database hosted on Redshift and helping the technology team of the start-up Sparkify to have a robust ETL pipeline extracting data from S3 Sparkify Bucket on AWS, and insert them into staging tables, and finally, transform the data and choose specific data prior inserting into fact/dimension tables ####

## Required installation:
- Python:
You can follow this [link](https://www.python.org/downloads/) to download and install Python based on your preferences. 

- Jupyter Notebook:
You can follow this [link](https://jupyter.org/install) to install Jupyter Notebook , in case you have Python already installed on your machine.
Or, you can install [Anaconda](https://docs.anaconda.com/anaconda/install/), and use Jupyter Notebook through it


## Design:

1- The mentioned DB consists of **5 tables, one fact table and four dimension tables**. The fact table "SongPlays" consists of 9 columns, which are "**songplay_id**, start_time, user_id, level, **song_id, artist_id**, session_id, location, user_agent". Songplay_id Column is a SERIAL column, and song_id and artist_id Columns are getting their values based on an inner join between ARTISTS table and Songs table with three conditions on the title of the song, name of the artist and the duration of the song. Additionally, the four dimension tables are consisting of the following columns respectively: 

- USERS Table "users in the app" - (user_id, first_name, last_name, gender, level)
- SONGS Table "songs in music database" - (song_id, title, artist_id, year, duration)
- ARTISTS Table "artists in music database" - (artist_id, name, location, latitude, longitude)
- TIME Table "timestamps of records in songplays broken down into specific units" - (start_time, hour, day, week, month, year, weekday)

The reason behind choosing the Star Schema over Snowflake Schema are the following:
- It's simple for users to write, and databases to process queries which are written with simple inner joins between the facts and a small number of dimensions. 
- Star joins are simpler than possible in a snowflake schema. 
- Star schemas tend to perform the best in decision-support applications.
- Fast Aggregations.

2- The ETL Pipeline design was a straightforward process. The script, etl.py, which have the code to all functions and imported varaibles, runs in the terminal. The script connects to the Sparkify database, extracts and processes the **log_data** and **song_data**, and loads data into the five tables.

3- Finally, Here are a description of each file in the project and how to run these files:

- sql_queries.py --> A Python script contains of all the SQL queries of DROP Table, CREATE Table and INSERT STATEMENTS.

- create_tables.py --> A Python script imports two lists (create_table_queries, drop_table_queries) from sql_queries.py. In other words, this script is responsible to connect to Sparkify DB, and to drop the tables if they are exist, and create them from scratch.

- etl.ipynb --> a Jupyter Notebook contains the code to test read a sample file of **log_data** and a sample file of **song_data**. Also, to try to insert the REAL values in the newly created tables.

- etl.py --> A Python script responsible to real all **log_data** files and **song_data** files and load them into the newly created tables.

- test.ipynb --> A jupyter Notebook contains code to connect to Sparkify DB and test the creation of the tables and the newly inserted columns.

- Data Readiness.ipynb --> A newly created jupyter Notebook to discover the data, and run the essential scripts in order. For example, I used the following code the run any Python script used in this project: %run (python_script_name) --> %run create_tables.py

- data directoru --> Holding all the log_data and song_data files.


## Analytics Queries:

#### SELECT level, count(user_id) FROM users group by level;
- This query can show us how may users are free-subscription or paid-subscription users. The result of this query was **77 users with free-subscription, and only 19 paid-subscription users**. The Marketing Team should always up to gain profits more and more through subscriptions.

#### SELECT location, count(songplay_id) FROM songplays group by location order by count(songplay_id) desc;
- This query can show us locations where there are high traffic on Sparkify App ordring from the highest to the lowest. The result of this query was that the location "San Francisco-Oakland-Hayward, CA" was causing the highest traffic on the app with counts of 691. On the contrary, the location "Myrtle Beach-Conway-North Myrtle Beach, SC-NC" was causing the lowest traffic on the app with count of 1.


#### SELECT gender, count(user_id) FROM users group by gender;
- This query shows us the percentage of gender regarding our unique users we have on Sparkify App. the result of the query was 41 Male users, with 55 Female users.
