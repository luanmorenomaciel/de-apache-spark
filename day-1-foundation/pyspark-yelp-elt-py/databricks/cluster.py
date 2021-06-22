# import libraries
from os.path import abspath
from pyspark.sql import SparkSession
from pyspark import SparkConf

# set default location for warehouse
warehouse_location = abspath('spark-warehouse')

# main spark program
if __name__ == '__main__':

    # init session
    spark = SparkSession \
            .builder \
            .appName("etl-yelp-py") \
            .config("spark.sql.warehouse.dir", abspath('spark-warehouse')) \
            .enableHiveSupport() \
            .getOrCreate()

    # show configured parameters
    print(SparkConf().getAll())

    # set log level
    spark.sparkContext.setLogLevel("INFO")

    # set dynamic input file [hard-coded]
    # can be changed for input parameters [spark-submit]
    # mount point = blob storage
    get_users_file = "dbfs:/mnt/bs-stg-files/users/*.json"
    get_business_file = "dbfs:/mnt/bs-stg-files/business/*.json"
    get_reviews_file = "dbfs:/mnt/bs-stg-files/reviews/*.json"

    # read user data
    df_user = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .option("header", "true") \
        .json(get_users_file)

    # read business data
    df_business = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .option("header", "true") \
        .json(get_business_file)

    # read review data
    df_review = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .option("header", "true") \
        .json(get_reviews_file)

    # get number of partitions
    # [25], [16], [48]
    print(df_user.rdd.getNumPartitions())
    print(df_business.rdd.getNumPartitions())
    print(df_review.rdd.getNumPartitions())

    # print schema of dataframe
    df_user.printSchema()
    df_business.printSchema()
    df_review.printSchema()

    # display data
    df_user.show()
    df_business.show()
    df_review.show()

    # count rows
    df_user.count()
    df_business.count()
    df_review.count()

    # register df into sql engine
    df_business.createOrReplaceTempView("business")
    df_user.createOrReplaceTempView("user")
    df_review.createOrReplaceTempView("review")

    # sql join into a new [df]
    df_join = spark.sql("""
        SELECT u.user_id,
               u.name AS user,
               u.average_stars AS user_avg_stars,
               u.useful AS user_useful, 
               u.review_count AS user_review_count,
               u.yelping_since,
               b.business_id,
               b.name AS business,
               b.city,
               b.state,
               b.stars AS business_stars,
               b.review_count AS business_review_count,
               r.useful AS review_useful,
               r.stars AS review_stars,
               r.date AS date
        FROM review AS r
        INNER JOIN business AS b
        ON r.business_id = b.business_id
        INNER JOIN user AS u
        ON u.user_id = r.user_id
    """)

    # show & count df
    df_join.explain()
    df_join.count()

    # show df
    df_join.show()

    # stop session
    # databricks will terminate automatically
    # spark.stop()
