# Apache Spark [Operator] & Apache Airflow [2.0] on Kubernetes

### configure minio cli to access storage
```sh
# install minio cli client
brew install minio/stable/mc

# minio configuration
mc config host add minio http://localhost:9000 YOURACCESSKEY YOURSECRETKEY

# list info
mc ls minio
mc tree minio
```

### configure apache spark [local] development
```sh
# install scala
brew install scala

# install spark [locally]
# venv using requirements [file]
brew install apache-spark

# verify installation location
brew info apache-spark

# verify pyspark version
pyspark --version

# spark-shell cli
spark-shell
```

### jars for installation [folder]
```sh
# libraries to copy to jars folder
aws-java-sdk-1.7.4.jar
hadoop-aws-2.7.3.jar
delta-core_2.12-0.7.0.jar
```

### submit application locally for test
```sh
# submit spark application for execution
spark-submit \
--conf spark.hadoop.fs.s3a.endpoint=http://localhost:9000 \
--conf spark.hadoop.fs.s3a.access.key=YOURACCESSKEY \
--conf spark.hadoop.fs.s3a.secret.key=YOURSECRETKEY \
--conf spark.hadoop.fs.s3a.path.style.access=True \
--conf spark.hadoop.fs.s3a.fast.upload=True \
--conf spark.hadoop.fs.s3a.connection.maximum=100 \
--conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
--conf spark.delta.logStore.class=org.apache.spark.sql.delta.storage.S3SingleDriverLogStore \
--conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
--conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
/Users/luanmorenomaciel/BitBucket/airflow/spark/pr-elt-business/pr-elt-business.py
```

### containerize [spark] app
```sh
# location of dockerfile [build image]
Dockerfile

# build image
docker build . -t owshq-pr-elt-business:3.0.0

# tag image
docker tag owshq-pr-elt-business:3.0.0 owshq/owshq-pr-elt-business:3.0.0

# push image to registry
docker push owshq/owshq-pr-elt-business:3.0.0

# remove old entries
docker rmi $(docker images --filter "dangling=true" -q --no-trunc) -f
```

### install and configure spark operator [spark-on-k8s]
```sh
# install spark operator 
helm repo update
helm install spark spark-operator/spark-operator --namespace processing
helm ls -n processing

# create & verify cluster role binding perms
k apply -f /Users/luanmorenomaciel/BitBucket/airflow/spark/crb-spark-operator-airflow-orchestrator.yaml -n orchestrator
k apply -f /Users/luanmorenomaciel/BitBucket/airflow/spark/crb-spark-operator-airflow-processing.yaml -n processing
k describe clusterrolebinding crb-spark-operator-airflow-orchestrator
k describe clusterrolebinding crb-spark-operator-airflow-processing

# deploy spark application [kubectl] for testing purposes
# eventually trigger this application using airflow
k apply -f /Users/luanmorenomaciel/BitBucket/airflow/dags/pr-elt-business.yaml -n processing

# get yaml detailed info
# verify submit
k get sparkapplications
k get sparkapplications pr-elt-business -o=yaml
k describe sparkapplication pr-elt-business

# port forward to spark ui
POD=pr-elt-business-driver
k port-forward $POD 4040:4040

# housekeeping
k delete SparkApplication pr-elt-business -n processing
k delete clusterrolebinding crb-spark-operator-airflow-orchestrator
k delete clusterrolebinding crb-spark-operator-airflow-processing
helm uninstall spark -n processing
```