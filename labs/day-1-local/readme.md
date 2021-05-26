### Data Engineer with Spark 3.0 ~ [local application]

For this application we have to setup all local environment, like below:

https://github.com/luanmorenomaciel/de-apache-spark/blob/main/day-1-foundation/readme.md

We going to use pycharm as our programming IDE.

All files will need to be in your local, in this case we going to use movies folder and ratings folder to read json files, please change the location for your local disk.

This application will:

1. show our cluster configured parameters
2. set logging as INFO = all, can be WARN = only warnings and ERROR = only errors
3. create dataframe and read files from json [movies]
4. create dataframe and read files from json [ratings]
5. print schemas and partitions
6. create materialized views in sql engine based on dataframes
7. create dataframe using spark.sql using join from the materialized views
8. display the join dataframe
9. writing data in your local disk as parquet
10. close spark application


and now lets run using spark-submit, don't forget to change your application location.

spark-submit \
--master local \
/Users/mateusoliveira/mateus/DataEngineeringWork/OwsHQ/Projects/development/bitbucket-mateus/spark-application-lab/local.py
