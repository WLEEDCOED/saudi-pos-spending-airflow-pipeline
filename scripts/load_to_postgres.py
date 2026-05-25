import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text


PROCESSED_DATA_PATH = Path("/opt/airflow/project/data/processed")
SQL_PATH = Path("/opt/airflow/project/sql")

CREATE_TABLES_FILE = SQL_PATH / "create_tables.sql"

DIM_DATE_FILE = PROCESSED_DATA_PATH / "dim_date.csv"
DIM_CITY_FILE = PROCESSED_DATA_PATH / "dim_city.csv"
DIM_SECTOR_FILE = PROCESSED_DATA_PATH / "dim_sector.csv"
FACT_POS_FILE = PROCESSED_DATA_PATH / "fact_pos_transactions_model.csv"

DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "postgres_dw"
DB_PORT = "5432"
DB_NAME = "saudi_pos_dw"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


def load_csv(file_path):
    return pd.read_csv(file_path)


def main():
    print("Starting PostgreSQL loading for star schema...")

    print("Connecting to PostgreSQL data warehouse...")
    engine = create_engine(DATABASE_URL)

    print("Reading create_tables.sql...")
    with open(CREATE_TABLES_FILE, "r", encoding="utf-8") as file:
        create_tables_sql = file.read()

    print("Creating star schema tables...")
    with engine.begin() as connection:
        connection.execute(text(create_tables_sql))

    print("Reading modeled data files...")
    dim_date = load_csv(DIM_DATE_FILE)
    dim_city = load_csv(DIM_CITY_FILE)
    dim_sector = load_csv(DIM_SECTOR_FILE)
    fact_pos = load_csv(FACT_POS_FILE)

    dim_date["date"] = pd.to_datetime(dim_date["date"]).dt.date

    print(f"dim_date rows: {dim_date.shape[0]}")
    print(f"dim_city rows: {dim_city.shape[0]}")
    print(f"dim_sector rows: {dim_sector.shape[0]}")
    print(f"fact_pos_transactions rows: {fact_pos.shape[0]}")

    print("Loading dimension tables...")
    dim_date.to_sql(
        "dim_date",
        engine,
        if_exists="append",
        index=False,
        chunksize=1000,
    )

    dim_city.to_sql(
        "dim_city",
        engine,
        if_exists="append",
        index=False,
        chunksize=1000,
    )

    dim_sector.to_sql(
        "dim_sector",
        engine,
        if_exists="append",
        index=False,
        chunksize=1000,
    )

    print("Loading fact table...")
    fact_pos.to_sql(
        "fact_pos_transactions",
        engine,
        if_exists="append",
        index=False,
        chunksize=1000,
    )

    print("✅ Star schema loaded to PostgreSQL successfully.")


if __name__ == "__main__":
    main()