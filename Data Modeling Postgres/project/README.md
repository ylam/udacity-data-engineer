# Understand our customers and their playlist at Sparkify 

Sparkify is a music streaming app and we like to better serve our customers by providing recommendations on new songs that users may like. When users listen to music from us we track metadata about them and the song they listen to. To understand them our business users would like to determine whether there are relationships between the songs and users that they listen to. 

## Design and Solution

As a data engineer I work on building a star schema data model. My goal is to collect the data from the application logs and song list played. Once data is collected then I need to insert them to tables in a database so it is easily discoverable with simple queries to answer many business questions. Below is the star schema with the following tables.

**Dimension tables**
    * songs
    * artists
    * users
    * time

**Fact table**
    * songs play

To populate songs and artists tables I collect from a song dataset which provides me the songs and artists information. I separate the data to two tables because for querying the business analysts may only want to know more about the songs or artists. 

My next source of data is from the Sparkify's application log which has user information. I use this to populate the users and time dimension tables. This dimension will help the business users to filter about the user types and specificy the time range of data that they like to investigate. 

Last is populating the fact table which needs data from song dataset and user's song list. I wrote a query which gets all the songs and artists and attempt to match any played songs if there is a match of song title, artist and duration. 

## Steps to build and populate data mart

**Requirements**
1. Python 3.6.3
2. Install dependencies from requirements.txt

**Run**
1. python create_tables.py
2. python etl.py
