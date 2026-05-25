
# Saudi POS Spending Airflow Pipeline

An end-to-end Data Engineering project that extracts, transforms, models, validates, and loads Saudi Point of Sale (POS) spending data using Apache Airflow, Docker, PostgreSQL, Python, and Pandas.

The project focuses on building a Dockerized data pipeline with Airflow orchestration, star schema data modeling, data quality checks, and SQL analytics.

---

## Project Overview

This pipeline processes Saudi POS spending data by city and sector. It extracts raw data, transforms it into an analytics-ready format, enriches it with city-region mapping data, models it into a star schema, validates data quality, and loads the final tables into PostgreSQL.

---

## Tech Stack

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Apache Airflow
- Docker
- Docker Compose
- SQL
- Git & GitHub

---

## Data Sources

The project uses two data sources:

1. **Saudi POS Transactions Data**
   - Date
   - Indicator
   - Sector
   - City
   - Value

2. **City Region Mapping**
   - City
   - Region
   - City Type

This allows analysis by city, region, sector, and time.


## Pipeline Architecture

```text
Saudi POS Data
      ↓
Extract
      ↓
Transform
      ↓
Data Modeling
      ↓
Data Quality Checks
      ↓
Load to PostgreSQL
      ↓
SQL Analytics
````

---

## Airflow DAG

<img width="1348" height="383" alt="image" src="https://github.com/user-attachments/assets/a004ffcb-1b23-4fba-acda-6a7d6dbf28ac" />


```text
saudi_pos_spending_pipeline
```

Task flow:

```text
extract_data
    ↓
transform_data
    ↓
model_data
    ↓
run_quality_checks
    ↓
load_to_postgres
```

---

## Project Structure

```text
saudi-pos-spending-airflow-pipeline/
│
├── dags/
│   └── saudi_pos_pipeline_dag.py
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── model_data.py
│   ├── quality_checks.py
│   └── load_to_postgres.py
│
├── sql/
│   ├── create_tables.sql
│   └── business_queries.sql
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Data Model

The project uses a star schema design.

```text
                 dim_date
                    │
                    │
dim_city ─── fact_pos_transactions ─── dim_sector
```

### Tables

| Table                   | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| `dim_date`              | Date attributes such as year, month, quarter, day name |
| `dim_city`              | City, region, and city type                            |
| `dim_sector`            | POS sector information                                 |
| `fact_pos_transactions` | POS transaction metrics                                |

---

## Final Warehouse Tables

```text
dim_date: 270 rows
dim_city: 12 rows
dim_sector: 18 rows
fact_pos_transactions: 7,830 rows
```

---

## Data Quality Checks

The pipeline validates:

* Empty tables
* Missing values
* Unique primary keys
* Unique fact table composite key
* Negative numeric values
* Foreign key consistency

Validated relationships:

```text
fact_pos_transactions.date_id → dim_date.date_id
fact_pos_transactions.city_id → dim_city.city_id
fact_pos_transactions.sector_id → dim_sector.sector_id
```

---

## Key Results

The pipeline processed:

```text
31,262 raw records
7,830 modeled fact records
270 dates
12 cities
18 sectors
```

Sample insight:

```text
Top cities by POS transaction value:
1. Riyadh
2. Other
3. Jeddah
4. Dammam
5. Makkah
```

---

## Sample SQL Query

```sql
SELECT
    c.region,
    c.city,
    ROUND(SUM(f.transaction_value_thousand_sar), 2) AS total_value_thousand_sar,
    ROUND(SUM(f.transaction_count_thousand), 2) AS total_transactions_thousand,
    ROUND(AVG(f.avg_transaction_value_sar), 2) AS avg_transaction_value_sar
FROM fact_pos_transactions f
JOIN dim_city c
    ON f.city_id = c.city_id
WHERE c.city <> 'Total'
GROUP BY
    c.region,
    c.city
ORDER BY total_value_thousand_sar DESC
LIMIT 10;
```

---

## How to Run

### 1. Start Airflow and PostgreSQL

```bash
docker compose up airflow-init
docker compose up -d
```

### 2. Open Airflow

```text
http://localhost:8080
```

Login:

```text
Username: admin
Password: admin
```

### 3. Run the DAG

Trigger this DAG from the Airflow UI:

```text
saudi_pos_spending_pipeline
```

### 4. Verify PostgreSQL Data

```bash
docker exec -it saudi_pos_postgres_dw psql -U postgres -d saudi_pos_dw
```

```sql
SELECT COUNT(*) FROM fact_pos_transactions;
```

Expected result:

```text
7830
```

---

## Business Questions Answered

* Which cities have the highest POS transaction value?
* Which regions have the highest consumer spending?
* Which sectors generate the most transaction value?
* What is the monthly and yearly spending trend?
* What is the average transaction value by city?
* What are the top city-sector combinations?

---

## Skills Demonstrated

* Data Engineering
* ETL Pipelines
* Apache Airflow
* Docker
* PostgreSQL
* Star Schema Data Modeling
* Multi-source Data Integration
* Data Quality Validation
* SQL Analytics
* Python and Pandas

---

## Future Improvements

* Add population data by city or region
* Calculate spending per capita
* Add CPI or inflation data
* Build a Streamlit dashboard
* Add incremental loading
* Add dbt transformations
* Add automated testing

---

## Author

**WLEEDCOED**

GitHub: [https://github.com/WLEEDCOED](https://github.com/WLEEDCOED)

```
```
