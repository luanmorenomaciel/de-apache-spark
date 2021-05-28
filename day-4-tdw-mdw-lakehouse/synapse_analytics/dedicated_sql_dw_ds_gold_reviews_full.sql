-- pool = pythianpool

-- select count rows
-- 434.170.658
SELECT COUNT(*) FROM ds_gold_reviews_full

-- query to test performance
-- first execution = 15 seconds
-- second execution = 4 seconds
SELECT TOP 10
    store_name,
    store_city,
    COUNT(*) AS Q
FROM dbo.ds_gold_reviews_full
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC