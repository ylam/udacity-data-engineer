# Understand our customers and their playlist at Sparkify 

Sparkify is a music streaming app and we like to better serve our customers by providing recommendations on new songs that users may like. When users listen to music from us we track metadata about them and the song they listen to. To understand them our business users would like to determine whether there are relationships between the songs and users that they listen to. 

## Datasets
We have two datasets that we source namely song and log dataset. Both datasets are in JSON file format which we leverage panda's read_json function to parse these datasets so we can import into our data marts.

**Song Dataset** 
To get song information and its artist we download data from a repository called (Million Song dataset)[]. This song dataset is important as it provides us additional information to the songs that our users listen to. The dataset is provided as a JSON file with an example of the format below.

```
{
  "num_songs": 1,
  "artist_id": "ARJIE2Y1187B994AB7",
  "artist_latitude": null,
  "artist_longitude": null,
  "artist_location": "",
  "artist_name": "Line Renaud",
  "song_id": "SOUPIRU12A6D4FA1E1",
  "title": "Der Kleine Dompfaff",
  "duration": 152.92036,
  "year": 0
}
```

**Log Dataset**
The log dataset shows activities that are performed by our users. 

```
{
  "artist": null,
  "auth": "Logged In",
  "firstName": "Walter",
  "gender": "M",
  "itemInSession": 0,
  "lastName": "Frye",
  "length": null,
  "level": "free",
  "location": "San Francisco-Oakland-Hayward, CA",
  "method": "GET",
  "page": "Home",
  "registration": 1540919166796,
  "sessionId": 38,
  "song": null,
  "status": 200,
  "ts": 1541105830796,
  "userAgent": "\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\"",
  "userId": "39"
}
```

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
