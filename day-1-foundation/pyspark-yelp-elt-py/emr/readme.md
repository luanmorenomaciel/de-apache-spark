# Amazon EMR ~ Apache Spark

[create spark job](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-spark-submit-step.html)
[submit jobs remotely](https://aws.amazon.com/premiumsupport/knowledge-center/emr-submit-spark-job-remote-cluster/)

> * deployment option = aws cloud formation & terraform 
> * account = one-way-solution
> * ohio [us-east-2]
> * s3 bucket = owshq-processing-zone
> * name = owshq-apache-spark
> * launch mode = cluster
> * release = emr-6.3.0
> * applications = spark: spark 3.1.1 on hadoop 3.2.1 yarn with and zeppelin 0.9.0
> * instance type = m4.large [3 + 1 = 4]
> * time to provision = [~ 15 min]
 
### verify storage on aws ~ [s3]
```sh
# s3 = storage
# bucket = owshq-processing-zone
folder = files

# protocols for loading data
# used for multi-part uploads
# https://stackoverflow.com/questions/33356041/technically-what-is-the-difference-between-s3n-s3a-and-s3
# https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-plan-file-systems.html
s3 = block-based overlay on top of amazon s3
s3n [up to 5 gb file size] & s3a [up to 5 tb file size, higher performance] = object-based
```

### submit a job into [amazon emr]
```sh
# steps page = add step
# step type = spark application
# app name = emr-job-batch-etl-yelp-py
# deploy mode = cluster
# application location = s3://owshq-processing-zone/app/cluster.py

# log files = after 3~5 minutes of job execution

# yarn
https://p-1fmjlk55pn5qh.emrappui-prod.us-east-2.amazonaws.com/applicationhistory

# spark history server
https://p-1fmjlk55pn5qh.emrappui-prod.us-east-2.amazonaws.com/shs/
```

### total time spent
```sh
# time taken to process
1 hour, 58 minutes
```