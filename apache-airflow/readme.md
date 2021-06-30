# Apache Airflow [2.0] on Kubernetes
> deploying and authoring data pipelines [dags]

### access airflow ui
```sh
# access web server pod
kubectl port-forward svc/airflow-webserver 8787:8080 --namespace orchestrator
```

### set up storage connection ~ [minio]
```sh
# create new connection with minio
# conn id = minio
# conn type = s3
# add the following line on extra 
{ "aws_access_key_id": "YOURACCESSKEY", "aws_secret_access_key": "YOURSECRETKEY", "host": "http://minio.deepstorage.svc.Cluster.local:9000"}
```

### set up database connection ~ [yugabytedb]
```sh
# create new connection with yugabytedb
# conn id = yugabytedb_ysql
# conn type = postgres
host = yb-tservers.database.svc.cluster.local
schema = owshq
login = yugabyte
password = yugabyte
port = 5433
```

### set up k8s & spark connection and permissions ~ [spark operator]
```sh
# create new connection with kubernetes [k8s]
# conn id = minikube
# conn type = kubernetes cluster connection
# in cluster configuration ~ [v]

# create spark operator cluster role binding for namespaces:
# - orchestrator
# - processing
```

### basic airflow [cli] commands
```sh
# log into container
# activate virtual env [venv]
POD=airflow-web-6c576777b-85n25
k exec $POD -c airflow-web -i -t -- bash
source /opt/bitnami/airflow/venv/bin/activate

# main cli commands
airflow -h
airflow users

# list dags
airflow dags list

# list tasks within dag
airflow tasks list test-data-pipeline

# test specific task of a dag
airflow tasks test test-data-pipeline print_date 2020-03-20
airflow tasks test s3-etl-business-json create_postgres_tb 2020-03-20

# trigger dag using cli
airflow dags trigger -e 2020-03-20 test-data-pipeline

# leave the venv
deactivate
```

### access [postgres] metadata service
```sh
# log into container
k exec airflow-postgresql-0 -i -t -- bash

# access postgres db
# pwd = bn_airflow
psql bitnami_airflow bn_airflow

# dags 
select * from dag;
```