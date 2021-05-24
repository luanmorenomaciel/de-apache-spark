# Apache Spark [Operator] on Kubernetes [K8S] - [spark-on-k8s]

[spark + s3 select](https://min.io/resources/docs/Spark-S3Select.pdf)

### configure minio cli to access storage
```sh
# install minio cli client
brew install minio/stable/mc
brew upgrade minio/stable/mc

# minio configuration
mc config host add minio http://20.72.90.44:9000 YOURACCESSKEY YOURSECRETKEY

# list info
# owshq-processing-zone
mc ls minio
mc tree minio
```

### jars for installation [folder]
```sh
# libraries to copy to jars folder
# local environment [copy]
# [jars loc] = /usr/local/lib/python3.9/site-packages/pyspark/jars 
# cp aws-java-sdk-1.7.4.jar /usr/local/lib/python3.9/site-packages/pyspark/jars 
# cp hadoop-aws-2.7.3.jar /usr/local/lib/python3.9/site-packages/pyspark/jars
# cp postgresql-42.2.19.jar /usr/local/lib/python3.9/site-packages/pyspark/jars
aws-java-sdk-1.7.4.jar
hadoop-aws-2.7.3.jar
postgresql-42.2.19.jar
```

### containerize [spark] app
```sh
# location = /Users/luanmorenomaciel/BitBucket/apache-spark/day-1-foundation/pyspark-yelp-elt-py/k8s_operator

# app name = batch-etl-yelp-py
# location of dockerfile [build image]
Dockerfile

# build image
# tag image
# push image to registry
docker build . -t batch-etl-yelp-py:3.0.0
docker tag batch-etl-yelp-py:3.0.0 owshq/batch-etl-yelp-py:3.0.0
docker push owshq/batch-etl-yelp-py:3.0.0
```

### install and configure spark operator [spark-on-k8s]
```sh
# select cluster to deploy 
kubectx aks-owshq-orion-dev
k get nodes

# install spark operator 
helm repo update
helm install spark spark-operator/spark-operator --namespace processing
helm ls -n processing
kgp -n processing

# create & verify cluster role binding perms
k apply -f /Users/luanmorenomaciel/BitBucket/apache-spark/pyspark-yelp-elt-py/k8s_operator/crb-spark-operator-processing.yaml -n processing
k describe clusterrolebinding crb-spark-operator-processing

# deploy spark application [kubectl] for testing purposes
# eventually trigger this application using airflow
# [deploy application]
kubens processing
k apply -f /Users/luanmorenomaciel/BitBucket/apache-spark/day-1-foundation/pyspark-yelp-elt-py/k8s_operator/batch-etl-yelp-py.yaml -n processing

# get yaml detailed info
# verify submit
k get sparkapplications
k get sparkapplications batch-etl-yelp-py -o=yaml
k describe sparkapplication batch-etl-yelp-py

# verify logs in real-time
k logs batch-etl-yelp-py-driver
k logs etl-yelp-py-df5e5479905332fa-exec-1

# port forward to spark ui
POD=batch-etl-yelp-py-driver
k port-forward $POD 4040:4040

# housekeeping
k delete SparkApplication batch-etl-yelp-py -n processing
k delete clusterrolebinding crb-spark-operator-processing
helm uninstall spark -n processing
```

### total time spent
```sh
# time taken to process
```