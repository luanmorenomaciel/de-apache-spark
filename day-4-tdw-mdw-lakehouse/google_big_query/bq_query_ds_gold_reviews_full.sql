SELECT COUNT(*) AS Q
FROM `silver-charmer-243611.OwsHQ.ds_gold_reviews_full`;

SELECT store_name,
    store_city,
    COUNT(*) AS Q
FROM `silver-charmer-243611.OwsHQ.ds_gold_reviews_full`
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC
LIMIT 10;