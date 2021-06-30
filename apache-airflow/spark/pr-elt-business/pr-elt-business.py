# import libraries
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf

# data processing using a data lake
# blob storage = azure
# s3 = amazon
# gcs = google
# minio = k8s
# hdfs = hadoop

# set config
conf = (
SparkConf()
    .set("spark.hadoop.fs.s3a.endpoint", "http://10.101.236.54:9000")
    .set("spark.hadoop.fs.s3a.access.key", "YOURACCESSKEY")
    .set("spark.hadoop.fs.s3a.secret.key", "YOURSECRETKEY")
    .set("spark.hadoop.fs.s3a.path.style.access", True)
    .set("spark.hadoop.fs.s3a.fast.upload", True)
    .set("spark.hadoop.fs.s3a.connection.maximum", 100)
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .set("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
    .set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)

# apply config
sc = SparkContext(conf=conf).getOrCreate()

# main spark program
if __name__ == '__main__':

    # init spark session
    # name of the app
    spark = SparkSession \
            .builder \
            .appName("pr-elt-business") \
            .getOrCreate()

    # set log level to info
    spark.sparkContext.setLogLevel("INFO")

    # read data frame [json]
    # get data from processing zone
    # list all files available
    df_business = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .json("s3a://processing/pr-elt-business/*.json")

    # display data into dataframe
    df_business.show()

    # print schema
    df_business.printSchema()

    # register df into sql engine
    df_business.createOrReplaceTempView("vw_business")

    # use sql engine to query data
    # select important columns
    df_business_sql = spark.sql("SELECT business_id, name, city, state, stars, review_count FROM vw_business")

    # display sql data frame
    df_business_sql.show()

    # save into delta format
    # curated zone
    df_business_sql.write.format("delta").mode("overwrite").save("s3a://delta/business/")

    # stop spark session
    spark.stop()
