Discuss the purpose of this database in context of the startup, Sparkify, and their analytical goals.
State and justify your database schema design and ETL pipeline.

--Query and then graph on a data frame?
(Credit)[https://gist.github.com/jakebrinkmann/de7fd185efe9a1f459946cf72def057e]
```
    import pandas as pd

    conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(host, port, dbname, username, pwd))
    sql = "select count(*) from table;"
    dat = pd.read_sql_query(sql, conn)
    conn = None
```

Story telling
What questions should we be asking?


Analytical goals
