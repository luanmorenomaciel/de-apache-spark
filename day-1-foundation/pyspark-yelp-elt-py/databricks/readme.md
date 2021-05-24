# Azure Databricks - Apache Spark

[schedule spark jobs](https://docs.databricks.com/jobs.html)  

> * deployment option = arm templates & terraform
> * option = create job
> * name = dbr-job-batch-etl-yelp-py
> * schedule type = manual
> * type = python
> * job location = [dbfs:/mnt/bs-stg-files/app/cluster.py]
> * configure new job cluster
> * cluster = 3 workers: standard_ds3_v2 ~ 8.2 (includes apache spark 3.1.1 & scala 2.12)
> * max concurrent runs = 1
 
### verify job execution
```sh
# job = dbr-job-batch-etl-yelp-py
# action = run 
# successfully started run of job "dbr-job-batch-etl-yelp-py"

# completed runs ~ view details
# view spark ui ~ history server
```

### total time spent
```sh
# time taken to process
39m 16s
```