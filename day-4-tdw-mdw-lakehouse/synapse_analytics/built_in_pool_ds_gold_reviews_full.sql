-- create database
-- DROP DATABASE owshq

CREATE DATABASE owshq
GO

-- use new database

-- create master key that will protect the credentials
-- DROP MASTER KEY ENCRYPTION BY PASSWORD = 'qq11ww22!!@@'

CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'qq11ww22!!@@'
GO

-- create external data source
-- DROP EXTERNAL DATA SOURCE eds_synapsefs_parquet

CREATE EXTERNAL DATA SOURCE eds_synapsefs_parquet
WITH (
    LOCATION = 'https://owshqcatalogsynapse.blob.core.windows.net'
);

-- create file format
-- DROP EXTERNAL FILE FORMAT eff_ds_gold_reviews_full

CREATE EXTERNAL FILE FORMAT eff_ds_gold_reviews_full
WITH (FORMAT_TYPE = PARQUET)

-- describe the types of the columns
-- create an accurate schema definition

EXEC sp_describe_first_result_set N'
SELECT *
FROM OPENROWSET
(
    BULK ''abfss://processing@owshqcatalogsynapse.dfs.core.windows.net/parquet/ds_gold_reviews_full'',
    FORMAT=''PARQUET''
) AS ds_gold_reviews_full';

-- create external table to reference parquet files
-- DROP EXTERNAL TABLE ds_gold_reviews_full

CREATE EXTERNAL TABLE ds_gold_reviews_full
(
    review_id VARCHAR(255),
    business_id VARCHAR(255),
    user_id VARCHAR(255),
    review_stars BIGINT,
    review_useful BIGINT,
    store_name VARCHAR(255),
    store_city VARCHAR(255),
    store_state VARCHAR(255),
    store_category VARCHAR(255),
    store_review_count BIGINT,
    store_stars FLOAT,
    user_name VARCHAR(255),
    user_average_stars FLOAT,
    user_importance VARCHAR(255)
)
WITH (
    LOCATION = '/processing/parquet/ds_gold_reviews_full',
    DATA_SOURCE = eds_synapsefs_parquet,
    FILE_FORMAT = eff_ds_gold_reviews_full
)
GO

-- select 1 row to test
SELECT TOP 1 * FROM ds_gold_reviews_full

-- select count rows
-- 434.170.658
SELECT COUNT(*) FROM ds_gold_reviews_full

-- query to test performance
-- 36 seconds
-- 25 seconds
SELECT TOP 10
    store_name,
    store_city,
    COUNT(*) AS Q
FROM dbo.ds_gold_reviews_full
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC