# Develop a Pipeline to Gather Analytics about Customer Behavior and Usage

Sparkify is providing music streaming to their customers and would like to retain and onboard more customers. To accomplish such mission Sparkify has a team of data and business analysts to review their customer behaviors. This team has questions like below to help decide where Sparkify should spend their resources to meet their mission.

* How many users are free versus paid users?
* What operating system do users stream?
* Where are most of the customers located?
* Do we have more male or female users?
* Which song is the most popular?
* Which artist is the most popular? 

As a data engineer we need to setup a tool that is easy for the data and business analysts team to answer such questions. We have decided to setup a data mart so this team can easily answer such questions. Our job is to populate this data mart with log data from our music streaming application and song data. Next I will describe the data set that we use to populate our staging tables and then we transform it to populate our dimension and fact tables.

## Describe data set
### Metadata about song and artist
JSON format files contain metadata about song and the artist of that song.
Sample of a single song file.

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

### User event data set log
JSON format files contain customer behaviors with which songs they listen to.
Sample of event data set log

```
{
    "artist": "Permanent",
    "auth": "Logged In",
    "firstName": "Sylvie",
    "gender": "F",
    "itemInSession": 0,
    "lastName": "Cruz",
    "length": 99.16036,
    "level": "free",
    "location": "Klamath Falls, OR",
    "method": "PUT",
    "page: "NextSong",
    "registration": 1541078,
    "sessionId": 438,
    "song": "Mercy: The Laundromat",
    "status": 200,
    "ts": 1541990258796",
    "userAgent": "Mozilla/5.0(Macintosh; Intel Mac OS x 10.9.4)",
    "userId": 53
}
```

To store metadata about song, artist and event data we create two staging tables. We load the data from the JSON files by using a copy command following instructions from link. Once the data is stored in staging tables we write insert queries with select statement to pull data from staging tables and load into our dimension and fact tables. 

## Infrastructure
To minimize upfront cost we decide to build the data mart on Amazon Web Services, AWS. We leverage a technology called Redshift which is a specialized relational database for data warehouse. It is easy to manage and we have used AWS's API to easily scafold a data warehouse on cloud. Our infrastructe as code can be found at [link](). 

## Steps to run code
1. Create a user in AWS and copy key and secret to [dwh.cfg file]().
2. Python 3.7.1 is installed in environment with modules `psycopg2` and `boto3` from [requirements.txt file]().
3. Scafold a redshift cluster follow steps in [lesson_setup_redshift_cluster notebook]()
4. Create tables in redshift cluster by running `python create_tables.py`
5. Populate staging, dimension and fact tables by running `python etl.py`

## References
1. Logic to convert epoch time to datetime with redshift [link](https://stackoverflow.com/questions/39815425/how-to-convert-epoch-to-datetime-redshift)
2. Infrastructure as code to build data mart with Redshift comes from L3 Execise 2 in lecture.
3. Copy command for generic JSON using auto with redshift [link](https://forums.aws.amazon.com/thread.jspa?messageID=538556)
4. Copy command documentation with redshift [link](https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-data-source-s3.html)
