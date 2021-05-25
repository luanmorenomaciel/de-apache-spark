# batching application running locally
# import libraries
from os.path import abspath
from pyspark.sql import SparkSession
from pyspark import SparkConf

# building main
if __name__ == '__main__':
    # init spark session
    spark = SparkSession \
        .builder \
        .appName("etl-batch-local-py") \
        .config("spark.sql.warehouse.dir", abspath('spark-warehouse')) \
        .enableHiveSupport() \
        .getOrCreate()

    # show configured parameters
    print(SparkConf().getAll())

    # set log level
    spark.sparkContext.setLogLevel("INFO")

    # read movie json
    df_movies = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .option("header", "true") \
        .json("/Users/mateusoliveira/mateus/DataEngineeringWork/OwsHQ/Training/apache-spark-labs/files/landing/movies/*.json")


    # read user json
    df_rating = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .option("header", "true") \
        .json("/Users/mateusoliveira/mateus/DataEngineeringWork/OwsHQ/Training/apache-spark-labs/files/landing/ratings/*.json")

    # print schema
    df_movies.printSchema()
    df_rating.printSchema()

    # display
    df_movies.show()
    df_rating.show()

    # get number of partitions
    print("number of partitions movies ", df_movies.rdd.getNumPartitions())
    print("number of partitions rating ", df_rating.rdd.getNumPartitions())


    # register df into sql engine
    df_movies.createOrReplaceTempView("movies")
    df_rating.createOrReplaceTempView("rating")


    # join into a new [df]
    df_join = spark.sql("""
        SELECT r.rating,
        m.dt_current_timestamp,
        m.original_title,
        m.release_date,
        m.title,
        m.user_id as movie_user_id,
        m.vote_count
        FROM movies AS m
        INNER JOIN rating AS r
        ON m.user_id = r.user_id
    """)

    # show df
    df_join.show()

    # write data in parquet files
    df_join.write.mode("overwrite").format("parquet").save("/Users/mateusoliveira/mateus/DataEngineeringWork/OwsHQ/Training/apache-spark-labs/files/processing/delta-join/")

    # stop spark session
    spark.stop()
