# Sparkify ETL data population using Apache Spark

## Introduction
We are growing our customer based but it is important that we continue to provide the best services possible to our customers. We have a lot of metadata about customer's behavior from our logs and to continue to provide value to our customer we need to convert this data into insight. 

We have built a team to consume, analyze and provide recommendations on how to best serve our customers. Our challenge is the need to get not only good quality data but also large data sets. We plan on leveraging Apache Spark which is great for working with large data sets. 

## Database design and ETL pipeline
Our ETL pipeline will extract from two datasets namely song and log. Below is a sample of their definition.

**Song dataset
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

**Log dataset
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

Our goal is to extract from the dataset into individual JSON files stored in Amazon Web Services' s3. The s3 data is flexible which can later be easily imported into a relational database if we like. In addition our analysts can use Apache Spark to load and query this data.

Below is an image of us successfully extracting and loading data into Amazone Web Services' s3. 

## Steps to build and populate s3 files
**Requirements**
1. Python 3.6.3
2. Install pyspark module
3. Have Amazon Web Services credentials namely key id and access key.
3. Create an s3 bucket and update in `etl.py`'s `output_data` s3 path

**Run**
1. python etl.py
