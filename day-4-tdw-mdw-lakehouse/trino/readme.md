# Data Virtualization using Trino & MinIO [Data Lake]

### connecting ingo trino coordinator [master]
```sh
# info to connect 
kubectx aks-owshq-orion-dev

kubens processing
# trino info [config]
kgp

# access coordinator
TRINO=trino-coordinator-54dc8d4c67-tqht4
kubectl exec $TRINO -it -- /usr/bin/trino
```

### virtualized queries using minio [s3]
```sql
-- show minio storage
-- http://20.72.90.44:9000/

-- list catalogs
show catalogs;

-- create schema
-- drop table if exists
CREATE SCHEMA minio.files;
DROP TABLE minio.files.ds_gold_reviews_full;

-- creating table from parquet files
CREATE TABLE minio.files.ds_gold_reviews_full
(
  review_id VARCHAR,
  business_id VARCHAR,
  user_id VARCHAR,
  review_stars BIGINT,
  review_useful BIGINT,
  store_name VARCHAR,
  store_city VARCHAR,
  store_state VARCHAR,
  store_category VARCHAR,
  store_review_count BIGINT,
  store_stars DOUBLE,
  user_name VARCHAR,
  user_average_stars DOUBLE,
  user_importance VARCHAR
)
WITH
(
  external_location = 's3a://curated/ds_gold_reviews_full/',
  format = 'parquet'
);

-- describe data
DESCRIBE minio.files.ds_gold_reviews_full;

-- query table
SELECT COUNT(*) AS Q FROM minio.files.ds_gold_reviews_full;

SELECT store_name,
    store_city,
    COUNT(*) AS Q
FROM minio.files.ds_gold_reviews_full
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC  
LIMIT 10;

/*
Query 20210527_210059_00022_gk5bq, FINISHED, 5 nodes
Splits: 228 total, 228 done (100.00%)
1:33 [158M rows, 70.4MB] [1.7M rows/s, 774KB/s]

Query 20210527_210251_00023_gk5bq, FINISHED, 5 nodes
Splits: 228 total, 228 done (100.00%)
1:06 [158M rows, 70.4MB] [2.39M rows/s, 1.06MB/s]
*/

-- ui 
http://localhost:9000/ui/
```