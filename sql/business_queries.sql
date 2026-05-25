-- =====================================================
-- Saudi POS Spending Business Queries
-- =====================================================

-- 1. Total records
SELECT
    COUNT(*) AS total_records
FROM fact_pos_transactions;


-- 2. Overall POS performance
SELECT
    ROUND(SUM(transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(SUM(transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(AVG(avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions;


-- 3. Top cities by transaction value
SELECT
    city,
    ROUND(SUM(transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(AVG(avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions
WHERE city <> 'Total'
GROUP BY city
ORDER BY total_value_thousand_sar DESC;


-- 4. Top sectors by transaction value
SELECT
    sector,
    ROUND(SUM(transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(AVG(avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions
WHERE sector <> 'Total'
GROUP BY sector
ORDER BY total_value_thousand_sar DESC;


-- 5. Monthly spending trend
SELECT
    DATE_TRUNC('month', date)::date AS month,
    ROUND(SUM(transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(transaction_count_thousand), 2) AS total_transactions_thousand
FROM fact_pos_transactions
WHERE city <> 'Total'
  AND sector <> 'Total'
GROUP BY DATE_TRUNC('month', date)
ORDER BY month;


-- 6. City and sector performance
SELECT
    city,
    sector,
    ROUND(SUM(transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(AVG(avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions
WHERE city <> 'Total'
  AND sector <> 'Total'
GROUP BY city, sector
ORDER BY total_value_thousand_sar DESC;


-- 7. Top 10 city-sector combinations
SELECT
    city,
    sector,
    ROUND(SUM(transaction_value_thousand_sar), 2) AS total_value_thousand_sar
FROM fact_pos_transactions
WHERE city <> 'Total'
  AND sector <> 'Total'
GROUP BY city, sector
ORDER BY total_value_thousand_sar DESC
LIMIT 10;


-- 8. Yearly spending trend
SELECT
    EXTRACT(YEAR FROM date)::int AS year,
    ROUND(SUM(transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(transaction_count_thousand), 2) AS total_transactions_thousand
FROM fact_pos_transactions
WHERE city <> 'Total'
  AND sector <> 'Total'
GROUP BY EXTRACT(YEAR FROM date)
ORDER BY year;