import pandas as pd
from pathlib import Path


PROCESSED_DATA_PATH = Path("/opt/airflow/project/data/processed")

DIM_DATE_FILE = PROCESSED_DATA_PATH / "dim_date.csv"
DIM_CITY_FILE = PROCESSED_DATA_PATH / "dim_city.csv"
DIM_SECTOR_FILE = PROCESSED_DATA_PATH / "dim_sector.csv"
FACT_POS_FILE = PROCESSED_DATA_PATH / "fact_pos_transactions_model.csv"


def check_not_empty(df, table_name):
    if df.empty:
        raise ValueError(f"{table_name} is empty")
    print(f"✅ {table_name} is not empty: {len(df)} rows")


def check_missing_values(df, table_name):
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        raise ValueError(f"{table_name} has missing values:\n{missing}")

    print(f"✅ {table_name}: No missing values")


def check_unique_key(df, key_column, table_name):
    duplicate_count = df[key_column].duplicated().sum()

    if duplicate_count > 0:
        raise ValueError(
            f"{table_name}: {duplicate_count} duplicate values in {key_column}"
        )

    print(f"✅ {table_name}: {key_column} is unique")


def check_composite_key(df, key_columns, table_name):
    duplicate_count = df.duplicated(subset=key_columns).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"{table_name}: {duplicate_count} duplicate composite keys found"
        )

    print(f"✅ {table_name}: Composite key is unique")


def check_no_negative_values(df, columns, table_name):
    for column in columns:
        negative_count = (df[column] < 0).sum()

        if negative_count > 0:
            raise ValueError(
                f"{table_name}: {negative_count} negative values in {column}"
            )

        print(f"✅ {table_name}: No negative values in {column}")


def check_foreign_key(fact_df, fact_column, dim_df, dim_column, relationship_name):
    missing_keys = set(fact_df[fact_column]) - set(dim_df[dim_column])

    if missing_keys:
        raise ValueError(
            f"{relationship_name}: {len(missing_keys)} missing keys found"
        )

    print(f"✅ {relationship_name}: All keys matched")


def main():
    print("Starting star schema data quality checks...")

    dim_date = pd.read_csv(DIM_DATE_FILE)
    dim_city = pd.read_csv(DIM_CITY_FILE)
    dim_sector = pd.read_csv(DIM_SECTOR_FILE)
    fact_pos = pd.read_csv(FACT_POS_FILE)

    tables = {
        "dim_date": dim_date,
        "dim_city": dim_city,
        "dim_sector": dim_sector,
        "fact_pos_transactions": fact_pos,
    }

    for table_name, df in tables.items():
        check_not_empty(df, table_name)
        check_missing_values(df, table_name)

    check_unique_key(dim_date, "date_id", "dim_date")
    check_unique_key(dim_city, "city_id", "dim_city")
    check_unique_key(dim_sector, "sector_id", "dim_sector")

    check_composite_key(
        fact_pos,
        ["date_id", "city_id", "sector_id"],
        "fact_pos_transactions",
    )

    check_no_negative_values(
        fact_pos,
        [
            "transaction_count_thousand",
            "transaction_value_thousand_sar",
            "avg_transaction_value_sar",
        ],
        "fact_pos_transactions",
    )

    check_foreign_key(
        fact_pos,
        "date_id",
        dim_date,
        "date_id",
        "fact_pos_transactions.date_id → dim_date.date_id",
    )

    check_foreign_key(
        fact_pos,
        "city_id",
        dim_city,
        "city_id",
        "fact_pos_transactions.city_id → dim_city.city_id",
    )

    check_foreign_key(
        fact_pos,
        "sector_id",
        dim_sector,
        "sector_id",
        "fact_pos_transactions.sector_id → dim_sector.sector_id",
    )

    print("✅ All star schema data quality checks passed successfully.")


if __name__ == "__main__":
    main()