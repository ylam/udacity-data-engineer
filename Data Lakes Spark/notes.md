Lesson 2: Data Wrangling with Spark

Lesson overview

Functional programming
    language: Scala

    Application programming in Java, R and Python

    PySpark - programming interface

Functional Programming Style
Map -> Shuffle -> Reduce

Functional progamming for distributed computing
    Function - one answer

Procedural example

Need to run calculation in parallel
    Need pure function and not function in python

Bread factory
    input ingredients
    avoid unattended side effects
        i.e. if running machine cause temperature goes up

    avoid contamination of your ingredients

    Very careful on how you design inputs

    Build pure functions

    Copy of input data
        input data is immutable
        chaining functions

    Directed Acyclic Graph - lazy evaluation
        Look at the recipes before making
        Each step - multi-combo stages

    Maps and Lambda functions

Load data into Sparks
    JSON, CSV, HTML, XML files (data formats)

    Distributed Data Stores
        Amazon Web Services (AWS)
            Simple Storage Service
            S3 - storage

    Spark session
        SparkContext, SparkConf

    Import/Export Spark Data Frames

Data Wrangling with Spark Examples
Data Wrangling with DataFrames Extra Tips

General Functions
    select(): returns a new dataframe with the selected columns
    filter(): filters rows using the given condition
    where(): is just an alia for filter()
    groupBy(): groups the DataFrame using the specified columns, so we can run aggregation on them
    sort(): returns a new DataFrame sorted by the specified columns. By default the second paramter 'ascending' is True
    dropDuplicates(): returns a new DataFrame with unique rows based on all or just a subset of columns
    withColumn(): returns a new DataFrame by adding a column or replacing an existing column that has the same name. The first parameter is the name of the new column, the second is an expression of how to compute it.

Python and SQL
    go to query optimizer (Catalyst) / execution plan (DAG)

Resilient Distributed Data Set (RDD)
    Spark Version 1.3 DataFrame API
    Spark Version 2 - SQL

RDD - has more power but less flexibility because no catalyst

Lesson 4 
    Introduction to Data Lakes

    How Data Lakes work?
    Dake Lake Issues

    