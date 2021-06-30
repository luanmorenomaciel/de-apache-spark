# [START pre_requisites]
# create connectivity to kubernetes [minio] ~ in-cluster configuration
# files yelp_academic_dataset_business_2018.json and yelp_academic_dataset_business_2019.json inside of processing/pr-elt-business
# spark operator deployed on processing namespace
# remove spark application from namespace processing
# [END pre_requisites]

# [START import_module]
from os import getenv
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.amazon.aws.operators.s3_list import S3ListOperator
from airflow.providers.amazon.aws.operators.s3_delete_objects import S3DeleteObjectsOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
# [END import_module]

# [START env_variables]
PROCESSING_ZONE = getenv("PROCESSING_ZONE", "processing")
CURATED_ZONE = getenv("CURATED_ZONE", "delta")
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
with DAG(
    's3-pr-elt-business-spark-operator',
    default_args=default_args,
    schedule_interval='@daily',
    tags=['development', 's3', 'sensor', 'minio', 'spark', 'operator', 'k8s']
) as dag:
# [END instantiate_dag]

    # [START set_tasks]
    # verify if new data has arrived on processing bucket
    # connecting to minio to check (sensor)
    verify_file_existence_processing = S3KeySensor(
        task_id='verify_file_existence_processing',
        bucket_name=PROCESSING_ZONE,
        bucket_key='pr-elt-business/*.json',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

    # use spark-on-k8s to operate against the data
    # containerized spark application
    # yaml definition to trigger process
    pr_elt_business_spark_operator = SparkKubernetesOperator(
        task_id='pr_elt_business_spark_operator',
        namespace='processing',
        application_file='pr-elt-business.yaml',
        kubernetes_conn_id='minikube',
        do_xcom_push=True)

    # monitor spark application
    # using sensor to determine the outcome of the task
    # read from xcom tp check the status [key & value] pair
    monitor_spark_app_status = SparkKubernetesSensor(
        task_id='monitor_spark_app_status',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='pr_elt_business_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="minikube")

    # check if folder and file exists
    # delta zone for data lakehouse
    list_curated_s3_folder = S3ListOperator(
        task_id='list_curated_s3_folder',
        bucket=CURATED_ZONE,
        prefix='business/',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)

    # delete file yelp_academic_dataset_business_2018.json
    # remove files on folder
    delete_s3_file_processing_zone_2018 = S3DeleteObjectsOperator(
        task_id='delete_s3_file_processing_zone_2018',
        bucket=PROCESSING_ZONE,
        keys='pr-elt-business/yelp_academic_dataset_business_2018.json',
        aws_conn_id='minio',
        do_xcom_push=True)

    # delete file yelp_academic_dataset_business_2019.json
    # remove files on folder
    delete_s3_file_processing_zone_2019 = S3DeleteObjectsOperator(
        task_id='delete_s3_file_processing_zone_2019',
        bucket=PROCESSING_ZONE,
        keys='pr-elt-business/yelp_academic_dataset_business_2019.json',
        aws_conn_id='minio',
        do_xcom_push=True)
    # [END set_tasks]

    # [START task_sequence]
    verify_file_existence_processing >> pr_elt_business_spark_operator >> monitor_spark_app_status >> list_curated_s3_folder >> [delete_s3_file_processing_zone_2018, delete_s3_file_processing_zone_2019]
    # [END task_sequence]
