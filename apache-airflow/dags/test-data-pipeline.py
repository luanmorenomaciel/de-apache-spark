# [START import_module]
from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
# [END import_module]

# [START default_args]
default_args = {
    'owner': 'luan moreno m. maciel',
    'depends_on_past': False,
    'email': ['luan.moreno@owshq.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5)}
# [END default_args]

# [START instantiate_dag]
dag = DAG(
    'test-data-pipeline',
    default_args=default_args,
    start_date=datetime(2021, 3, 18),
    schedule_interval='@weekly',
    tags=['test', 'development', 'bash'])
# [END instantiate_dag]

# [START basic_task]
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag)
# [END basic_task]

# [START task_sequence]
t1 >> [t2]
# [END task_sequence]
