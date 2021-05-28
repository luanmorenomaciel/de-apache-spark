# Apache Hive [LLAP] as a Modern Data Warehouse [MDW]

> * deployment option = arm templates & terraform 
> * subscription = visual studio enterprise with msdn
> * resource group = owshqeastus2
> * name = owshq-apache-hive-llap
> * region = eastus2
> * cluster type = interactive query
> * version = interactive query 3.1.0 [hdi 4.0]
> * login = luanmoreno
> * pwd = Qq11ww22!!@@
> * ssh user = sshuser
> * primary storage = adls2
> * storage account = owshqcatalogsynapse
> * filesystem = owshq-apache-hive-llap
> * identity = uami-owshq-apache-spark [storage blob data owner]
> * head node = d13 v2 [2]
> * zookeeper node = a1 v2 [3]
> * worker node = d13 v2 [2]
> * total cost per hour = [2.90 USD] 
> * time to provision = [~ 15 min]

### apache hive llap [info]
```sh
# data is stored on azure data lake gen2 
# fastest driver abfs
# amount of rows = 434.170.658
abfss://processing@owshqcatalogsynapse.dfs.core.windows.net/orc/ds_gold_reviews_full

# cluster name = owshq-apache-hive-llap
# ambari
https://owshq-apache-hive-llap.azurehdinsight.net

# tez [processing engine v.2 of mapreduce]
https://owshq-apache-hive-llap.azurehdinsight.net/#/main/view/TEZ/tez_cluster_instance

# hive view 2.0
# other interfaces available to tap into apache hive
https://owshq-apache-hive-llap.azurehdinsight.net/#/main/view/HIVE/auto_hive20_instance
```

### creating structure on hive llap [live long and process]
```sql
--1 - creating table 
DROP TABLE IF EXISTS ds_gold_reviews_full;

CREATE EXTERNAL TABLE ds_gold_reviews_full
(
  review_id STRING,
  business_id STRING,
  user_id STRING,
  review_stars INT,
  review_useful INT,
  store_name STRING,
  store_city STRING,
  store_state STRING,
  store_category STRING,
  store_review_count INT,
  store_stars FLOAT,
  user_name STRING,
  user_average_stars FLOAT,
  user_importance STRING
 ) STORED AS ORC
 
-- 2 - load data from storage into orc table [434.170.658]
LOAD DATA INPATH 'abfss://processing@owshqcatalogsynapse.dfs.core.windows.net/orc/ds_gold_reviews_full' 
INTO TABLE ds_gold_reviews_full;

-- 3 - amount of records on the table
-- 434.170.658
SELECT COUNT(*) FROM ds_gold_reviews_full;

-- 4 verify properties
SHOW TBLPROPERTIES ds_gold_reviews_full;
DESCRIBE EXTENDED ds_gold_reviews_full;

-- first execution = 14 seconds
SELECT store_name,
    store_city,
    COUNT(*) AS Q
FROM ds_gold_reviews_full
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC
LIMIT 10;

-- first execution = 9 seconds
-- second execution = 9 seconds
set hive.execution.engine = tez;
set hive.llap.execution.mode = all;
set hive.vectorized.execution.enabled = true;
set hive.vectorized.execution.reduce.enabled = true;

SELECT store_name,
    store_city,
    COUNT(*) AS Q
FROM ds_gold_reviews_full
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC
LIMIT 10;

-- optimize query [statistics]
ANALYZE TABLE ds_gold_reviews_full COMPUTE STATISTICS FOR COLUMNS;

set hive.execution.engine = tez;
set hive.llap.execution.mode = all;
set hive.vectorized.execution.enabled = true;
set hive.vectorized.execution.reduce.enabled = true;

SELECT store_name,
    store_city,
    COUNT(*) AS Q
FROM ds_gold_reviews_full
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC
LIMIT 10;
```

