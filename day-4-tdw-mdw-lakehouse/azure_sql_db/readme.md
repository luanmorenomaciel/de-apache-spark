# Azure SQL DB as a Traditional Data Warehouse [TDW]

> * deployment option = arm templates & terraform
> * subscription = visual studio enterprise with msdn
> * server name = synapseowshq.database.windows.net
> * pricing tier = premium p1: 125 dtus
> * price per month = 465 usd

### azure sql db info
```sh
# premium tier - for io-intensive workloads
# enables the column store index capability
https://azure.microsoft.com/pt-br/blog/clustered-columnstore-index-in-azure-sql-database/

# scale-up resources during load time

# compare dtus against vcores option
https://docs.microsoft.com/en-us/azure/azure-sql/database/service-tiers-vcore?tabs=azure-portal
https://docs.microsoft.com/en-us/azure/azure-sql/database/migrate-dtu-to-vcore
```

### create tables upfront for better optimization
```sql
-- remove tables if exists
DROP TABLE IF EXISTS dm_users
DROP TABLE IF EXISTS dm_business
DROP TABLE IF EXISTS fact_reviews

-- create tables
CREATE TABLE dm_users
(
  user_id VARCHAR(100),
  name VARCHAR(100),
  review_count BIGINT,
  useful BIGINT,
  fans BIGINT,
  average_stars FLOAT,
  importance VARCHAR(100),
  yelping_since DATETIME
);

CREATE TABLE dm_business
(
  business_id VARCHAR(1000),
  name VARCHAR(1000),
  city VARCHAR(1000),
  state VARCHAR(1000),
  category VARCHAR(1000),
  subcategories VARCHAR(1000),
  review_count BIGINT,
  stars FLOAT
);

CREATE TABLE fact_reviews
(
  business_id VARCHAR(100),
  user_id VARCHAR(100),
  review_id VARCHAR(100),
  cool BIGINT,
  funny BIGINT,
  useful BIGINT,
  stars BIGINT,
  date DATE
);

-- create cci indexes for [olap] query optimization
CREATE CLUSTERED COLUMNSTORE INDEX cci_dm_users ON dm_users
CREATE CLUSTERED COLUMNSTORE INDEX cci_dm_business ON dm_business
CREATE CLUSTERED COLUMNSTORE INDEX cci_fact_reviews ON fact_reviews
```

### analytics queries
```sql
-- 2.929.573
SELECT COUNT(*)
FROM dbo.dm_users

-- 586.579
SELECT COUNT(*)
FROM dbo.dm_business

-- 81.931.119
SELECT COUNT(*)
FROM dbo.fact_reviews

-- verify azure sql db features
-- complex query for analytics
-- first execution = 10 rows retrieved starting from 1 in 25 s 798 ms (execution: 25 s 755 ms, fetching: 43 ms)
-- second execution = 10 rows retrieved starting from 1 in 20 s 335 ms (execution: 20 s 309 ms, fetching: 26 ms)
SELECT TOP 10
    business.name,
    business.city,
    COUNT(*) AS Q
FROM fact_reviews AS reviews
INNER JOIN dm_business AS business
ON reviews.business_id = business.business_id
INNER JOIN dm_users AS users
ON business.name = users.name
WHERE importance = 'rockstar'
GROUP BY business.name, business.city
ORDER BY Q DESC
```
