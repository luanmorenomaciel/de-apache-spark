# Google DataProc - Apache Spark

[running jobs in production for dataproc](https://cloud.google.com/blog/products/data-analytics/7-best-practices-for-running-cloud-dataproc-in-production)  
[tips for running long-running clusters](https://cloud.google.com/blog/products/data-analytics/10-tips-for-building-long-running-clusters-using-cloud-dataproc)  

> * deployment option = gcloud, deployment manager & terraform
> * subscription = owshq-luan-moreno
> * name = owshq-apache-spark
> * region = us-east1
> * zone = us-east1-c
> * cluster type = standard [1 master & multiple workers]
> * versioning = 2.0 [debian 10, hadoop 3.2, apache spark 3.1] 
> * component gateway = enable
> * machine family = general-purpose
> * series = n1
> * type = n1-standard-2 [2 vcpus & 7.5 gb] x [2]
> * access = allow api access of all gcp services
> * cloud storage location = us-east1
> * storage name = owshq-processing-zone
> * time to provision = [90 secs]

### interact with gcs using google [cloud shell]
```sh
# tool = gsutil 
gsutil ls gs://owshq-processing-zone/files
gsutil ls gs://owshq-processing-zone/files/users
gsutil ls gs://owshq-processing-zone/files/business
gsutil ls gs://owshq-processing-zone/files/reviews

# spark app [program]
gsutil ls gs://owshq-processing-zone/app
```

### submit a job on dataproc [apache spark]
```sh
# job name = dataproc-batch-etl-yelp-py
# region = us-east1
# cluster name = owshq-luan-moreno
# job type = pyspark
# python file loc = gs://owshq-processing-zone/app/cluster.py
gcloud dataproc jobs wait dataproc-batch-etl-yelp-py --project silver-charmer-243611 --region us-east1

# blade [1] = vm instances
# blade [2] = web interfaces ~ spark history server
https://uh6z66f5avfz5gkwxj5zux2xxu-dot-us-east1.dataproc.googleusercontent.com/sparkhistory/

# notebook = jupyter lab
```

### total time spent
```sh
# time taken to process
20 min 44 sec
```