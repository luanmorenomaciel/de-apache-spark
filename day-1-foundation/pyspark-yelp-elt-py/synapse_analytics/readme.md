# Azure Synapse Analytics - Apache Spark Pools

> * deployment option = arm templates & terraform
> * workspace = pythiansynapseworkspace
> * spark pools = pythian
 
### submit job to spark cluster
```sh
# develop area = apache spark job definition
# language = pyspark [python]
# job name = synapse-spark-pools-batch-etl-yelp-py
# main file = abfs://processing@owshqcatalogsynapse.dfs.core.windows.net/app/cluster.py

# apache spark pool = pythian
# version = 2.4
# executor size = medium [8 vcores & 56 gb of ram] 
# executors = 2

# submit job to execution
# monitoring web interface ~ monitor -> apache spark applications
```

### total time spent
```sh
# time taken to process
27m 50s
```