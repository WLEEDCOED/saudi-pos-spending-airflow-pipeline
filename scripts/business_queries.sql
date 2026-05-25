-- =====================================================
-- Saudi POS Spending Star Schema Business Queries
-- =====================================================

-- 1. Count records in each warehouse table
SELECT 'dim_date' AS table_name, COUNT(*) AS total_rows FROM dim_date
UNION ALL
SELECT 'dim_city' AS table_name, COUNT(*) AS total_rows FROM dim_city
UNION ALL
SELECT 'dim_sector' AS table_name, COUNT(*) AS total_rows FROM dim_sector
UNION ALL
SELECT 'fact_pos_transactions' AS table_name, COUNT(*) AS total_rows FROM fact_pos_transactions;


-- 2. Overall POS performance
SELECT
    ROUND(SUM(f.transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(SUM(f.transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(AVG(f.avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions f;


-- 3. Top cities by transaction value
SELECT
    c.city,
    c.region,
    ROUND(SUM(f.transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(f.transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(AVG(f.avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions f
JOIN dim_city c
    ON f.city_id = c.city_id
WHERE c.city <> 'Total'
GROUP BY
    c.city,
    c.region
ORDER BY total_value_thousand_sar DESC
LIMIT 10;


-- 4. Top regions by transaction value
SELECT
    c.region,
    ROUND(SUM(f.transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(f.transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(AVG(f.avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions f
JOIN dim_city c
    ON f.city_id = c.city_id
WHERE c.region NOT IN ('All Regions', 'Other')
GROUP BY c.region
ORDER BY total_value_thousand_sar DESC;


-- 5. Top sectors by transaction value
SELECT
    s.sector,
    ROUND(SUM(f.transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(f.transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(AVG(f.avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions f
JOIN dim_sector s
    ON f.sector_id = s.sector_id
WHERE s.sector <> 'Total'
GROUP BY s.sector
ORDER BY total_value_thousand_sar DESC
LIMIT 10;


-- 6. Monthly spending trend
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(f.transaction_count_thousand), 2) AS total_transactions_thousand
FROM fact_pos_transactions f
JOIN dim_date d
    ON f.date_id = d.date_id
JOIN dim_city c
    ON f.city_id = c.city_id
JOIN dim_sector s
    ON f.sector_id = s.sector_id
WHERE c.city <> 'Total'
  AND s.sector <> 'Total'
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- 7. City and sector performance
SELECT
    c.region,
    c.city,
    s.sector,
    ROUND(SUM(f.transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(f.transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(AVG(f.avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions f
JOIN dim_city c
    ON f.city_id = c.city_id
JOIN dim_sector s
    ON f.sector_id = s.sector_id
WHERE c.city <> 'Total'
  AND s.sector <> 'Total'
GROUP BY
    c.region,
    c.city,
    s.sector
ORDER BY total_value_thousand_sar DESC
LIMIT 20;


-- 8. Yearly spending trend
SELECT
    d.year,
    ROUND(SUM(f.transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(f.transaction_count_thousand), 2) AS total_transactions_thousand
FROM fact_pos_transactions f
JOIN dim_date d
    ON f.date_id = d.date_id
JOIN dim_city c
    ON f.city_id = c.city_id
JOIN dim_sector s
    ON f.sector_id = s.sector_id
WHERE c.city <> 'Total'
  AND s.sector <> 'Total'
GROUP BY d.year
ORDER BY d.year;