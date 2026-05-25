
DROP TABLE IF EXISTS fact_pos_transactions;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_city;
DROP TABLE IF EXISTS dim_sector;

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    quarter INTEGER,
    month_name VARCHAR(20),
    day_name VARCHAR(20)
);

CREATE TABLE dim_city (
    city_id INTEGER PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    city_type VARCHAR(50)
);

CREATE TABLE dim_sector (
    sector_id INTEGER PRIMARY KEY,
    sector VARCHAR(255) NOT NULL
);

CREATE TABLE fact_pos_transactions (
    date_id INTEGER REFERENCES dim_date(date_id),
    city_id INTEGER REFERENCES dim_city(city_id),
    sector_id INTEGER REFERENCES dim_sector(sector_id),
    transaction_count_thousand NUMERIC(18, 2),
    transaction_value_thousand_sar NUMERIC(18, 2),
    avg_transaction_value_sar NUMERIC(18, 2),
    PRIMARY KEY (date_id, city_id, sector_id)
);