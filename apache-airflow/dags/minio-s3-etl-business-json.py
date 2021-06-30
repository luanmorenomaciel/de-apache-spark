# TODO compare count of minio and yugabytedb

# [START pre_requisites]
# create connectivity to minio and yugabytedb on airflow ui [connections]
# file yelp_business.json inside of landing/business bucket on minio
# yugabytedb (postgres) database owshq created
# [END pre_requisites]

# [START import_module]
import pandas as pd
from minio import Minio
from os import getenv
from io import BytesIO
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.amazon.aws.operators.s3_list import S3ListOperator
from airflow.providers.amazon.aws.operators.s3_copy_object import S3CopyObjectOperator
from airflow.providers.amazon.aws.operators.s3_delete_objects import S3DeleteObjectsOperator
# [END import_module]

# [START env_variables]
MINIO = getenv("MINIO", "minio.deepstorage.svc.Cluster.local:9000")
ACCESS_KEY = getenv("ACCESS_KEY", "YOURACCESSKEY")
SECRET_ACCESS = getenv("SECRET_ACCESS", "YOURSECRETKEY")
YUGABYTEDB = getenv("YUGABYTEDB", "postgresql://yugabyte:yugabyte@yb-tservers.database.svc.Cluster.local:5433/owshq")
BUSINESS_ORIGINAL_FILE_LOCATION = getenv("BUSINESS_ORIGINAL_FILE_LOCATION", "files/business/yelp_academic_dataset_business_2.json")
LANDING_ZONE = getenv("LANDING_ZONE", "owshq-processing-zone")
PROCESSING_ZONE = getenv("PROCESSING_ZONE", "processing")
CURATED_ZONE = getenv("CURATED_ZONE", "curated")
CURATED_BUSINESS_CSV_FILE = getenv("CURATED_BUSINESS_CSV_FILE", "business/yelp_business.csv")
# [END env_variables]

# [START default_args]
default_args = {
    'owner': 'luan moreno m. maciel',
    'start_date': datetime(2021, 6, 25),
    'depends_on_past': False,
    'email': ['luan.moreno@owshq.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)}
# [END default_args]

# [START instantiate_dag]
dag = DAG(
    'minio-s3-etl-business-json',
    default_args=default_args,
    schedule_interval='@daily',
    tags=['development', 's3', 'sensor', 'minio', 'python', 'yugabytedb'])
# [END instantiate_dag]


# [START functions]
def read_business_json_data(ti):
    # airflow feature that allows the exchange messages for sharing states
    # defined by a key and value, to get access use the task id
    # ['business/yelp_business.json']
    get_xcom_file_name = ti.xcom_pull(task_ids=['list_file_s3'])
    print(get_xcom_file_name)
    print(type(get_xcom_file_name))

    # set up connectivity with minio storage
    client = Minio(MINIO, ACCESS_KEY, SECRET_ACCESS, secure=False)

    # download file from bucket
    # processing engine access processing bucket [always]
    # empty if nothing to process
    # reading xcom from list s3 task
    obj_business = client.get_object(
        PROCESSING_ZONE,
        get_xcom_file_name[0][0],
    )

    # read json file using pandas
    # select and output only 10 rows
    # convert to dictionary
    # reduce amount = .head(10000) [dataframe]
    df_business = pd.read_json(obj_business, lines=True)
    selected_data = df_business[["business_id", "name", "city", "state", "stars", "review_count"]].head(5000)
    selected_data.to_dict('records')

    # dataframe to csv - encode and buffer bytes
    csv_bytes = selected_data.to_csv(header=True, index=False).encode('utf-8')
    csv_buffer = BytesIO(csv_bytes)

    # writing into minio storage [curated zone]
    client.put_object(
        CURATED_ZONE,
        CURATED_BUSINESS_CSV_FILE,
        data=csv_buffer,
        length=len(csv_bytes),
        content_type='application/csv')


def write_business_dt_postgres():
    # set up connectivity with minio storage
    # minio.deepstorage.svc.Cluster.local:9000
    client = Minio(MINIO, ACCESS_KEY, SECRET_ACCESS, secure=False)

    # download file from bucket
    obj_business = client.get_object(CURATED_ZONE, CURATED_BUSINESS_CSV_FILE)

    # read file from curated zone
    df_business = pd.read_csv(obj_business)

    # insert pandas data frame into postgres db [sqlalchemy]
    # connect into postgres and ingest data
    #  adding method multi
    postgres_engine = create_engine(YUGABYTEDB)
    df_business.to_sql('business', postgres_engine, if_exists='append', index=False, chunksize=10)
# [END functions]


# [START set_tasks]
# verify if new file has landed into bucket
verify_file_existence_landing = S3KeySensor(
    task_id='verify_file_existence_landing',
    bucket_name=LANDING_ZONE,
    bucket_key='files/business/*.json',
    wildcard_match=True,
    timeout=18 * 60 * 60,
    poke_interval=120,
    aws_conn_id='minio',
    dag=dag)

# copy file from landing to processing zone
copy_s3_file_processed_zone = S3CopyObjectOperator(
    task_id='copy_s3_file_processed_zone',
    source_bucket_name=LANDING_ZONE,
    source_bucket_key=BUSINESS_ORIGINAL_FILE_LOCATION,
    dest_bucket_name=PROCESSING_ZONE,
    dest_bucket_key=BUSINESS_ORIGINAL_FILE_LOCATION,
    aws_conn_id='minio',
    dag=dag)

# list all files inside of a bucket [names]
# processing zone file listing
list_file_s3 = S3ListOperator(
    task_id='list_file_s3',
    bucket=PROCESSING_ZONE,
    prefix='files/business/',
    delimiter='/',
    aws_conn_id='minio',
    do_xcom_push=True,
    dag=dag)

# apply transformation [python function]
process_business_data = PythonOperator(
    task_id='process_business_data',
    python_callable=read_business_json_data,
    dag=dag)

# delete file from landing zone [old file]
delete_s3_file_landing_zone = S3DeleteObjectsOperator(
    task_id='delete_s3_file_landing_zone',
    bucket=LANDING_ZONE,
    keys=BUSINESS_ORIGINAL_FILE_LOCATION,
    aws_conn_id='minio',
    dag=dag)

# delete file from processed zone
delete_s3_file_processed_zone = S3DeleteObjectsOperator(
    task_id='delete_s3_file_processed_zone',
    bucket=PROCESSING_ZONE,
    keys=BUSINESS_ORIGINAL_FILE_LOCATION,
    aws_conn_id='minio',
    dag=dag)

# delete table to perform full load
drop_postgres_tb = PostgresOperator(
    task_id='drop_postgres_tb',
    postgres_conn_id='yugabytedb_ysql',
    sql=""" DROP TABLE IF EXISTS business; """,
    dag=dag)

# create table on postgres [if not exists] = yugabytedb [ysql]
create_postgres_tb = PostgresOperator(
    task_id='create_postgres_tb',
    postgres_conn_id='yugabytedb_ysql',
    sql="""
        CREATE TABLE IF NOT EXISTS business 
        (
            id SERIAL PRIMARY KEY, 
            business_id VARCHAR NOT NULL, 
            name VARCHAR NULL, 
            city VARCHAR NULL, 
            state VARCHAR NULL,
            stars NUMERIC NULL,
            review_count INTEGER NULL
        );""",
    dag=dag)

# write data into postgres database [yugabytedb]
# ingestion of [~ 2 million] rows on table
write_business_dt_yugabytedb = PythonOperator(
    task_id='write_business_dt_yugabytedb',
    python_callable=write_business_dt_postgres,
    dag=dag)
# [END set_tasks]

# [START task_sequence]
verify_file_existence_landing >> copy_s3_file_processed_zone >> list_file_s3 >> process_business_data >> delete_s3_file_landing_zone >> delete_s3_file_processed_zone >> drop_postgres_tb >> create_postgres_tb >> write_business_dt_yugabytedb
# [END task_sequence]
