import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("/opt/airflow/project/data/raw")
PROCESSED_DATA_PATH = Path("/opt/airflow/project/data/processed")

FACT_INPUT_FILE = PROCESSED_DATA_PATH / "fact_pos_transactions.csv"
CITY_MAPPING_FILE = RAW_DATA_PATH / "city_region_mapping.csv"

DIM_DATE_FILE = PROCESSED_DATA_PATH / "dim_date.csv"
DIM_CITY_FILE = PROCESSED_DATA_PATH / "dim_city.csv"
DIM_SECTOR_FILE = PROCESSED_DATA_PATH / "dim_sector.csv"
FACT_OUTPUT_FILE = PROCESSED_DATA_PATH / "fact_pos_transactions_model.csv"


def main():
    print("Starting data modeling...")

    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    fact_pos = pd.read_csv(FACT_INPUT_FILE)
    city_mapping = pd.read_csv(CITY_MAPPING_FILE)

    fact_pos["date"] = pd.to_datetime(fact_pos["date"])

    print(f"Fact input rows: {fact_pos.shape[0]}")
    print(f"City mapping rows: {city_mapping.shape[0]}")

    # -----------------------------
    # Build dim_date
    # -----------------------------
    dim_date = (
        fact_pos[["date"]]
        .drop_duplicates()
        .sort_values("date")
        .reset_index(drop=True)
    )

    dim_date["date_id"] = dim_date.index + 1
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["month_name"] = dim_date["date"].dt.month_name()
    dim_date["day_name"] = dim_date["date"].dt.day_name()

    dim_date = dim_date[
        [
            "date_id",
            "date",
            "year",
            "month",
            "day",
            "quarter",
            "month_name",
            "day_name",
        ]
    ]

    # -----------------------------
    # Build dim_city
    # -----------------------------
    dim_city = (
        fact_pos[["city"]]
        .drop_duplicates()
        .sort_values("city")
        .reset_index(drop=True)
    )

    dim_city = dim_city.merge(
        city_mapping,
        on="city",
        how="left"
    )

    dim_city["region"] = dim_city["region"].fillna("Unknown")
    dim_city["city_type"] = dim_city["city_type"].fillna("Unknown")

    dim_city["city_id"] = dim_city.index + 1

    dim_city = dim_city[
        [
            "city_id",
            "city",
            "region",
            "city_type",
        ]
    ]

    # -----------------------------
    # Build dim_sector
    # -----------------------------
    dim_sector = (
        fact_pos[["sector"]]
        .drop_duplicates()
        .sort_values("sector")
        .reset_index(drop=True)
    )

    dim_sector["sector_id"] = dim_sector.index + 1

    dim_sector = dim_sector[
        [
            "sector_id",
            "sector",
        ]
    ]

    # -----------------------------
    # Build modeled fact table
    # -----------------------------
    fact_model = fact_pos.merge(
        dim_date[["date_id", "date"]],
        on="date",
        how="left"
    )

    fact_model = fact_model.merge(
        dim_city[["city_id", "city"]],
        on="city",
        how="left"
    )

    fact_model = fact_model.merge(
        dim_sector[["sector_id", "sector"]],
        on="sector",
        how="left"
    )

    fact_model = fact_model[
        [
            "date_id",
            "city_id",
            "sector_id",
            "transaction_count_thousand",
            "transaction_value_thousand_sar",
            "avg_transaction_value_sar",
        ]
    ]

    # -----------------------------
    # Save modeled tables
    # -----------------------------
    dim_date.to_csv(DIM_DATE_FILE, index=False)
    dim_city.to_csv(DIM_CITY_FILE, index=False)
    dim_sector.to_csv(DIM_SECTOR_FILE, index=False)
    fact_model.to_csv(FACT_OUTPUT_FILE, index=False)

    print("Modeled tables saved successfully.")
    print(f"dim_date rows: {dim_date.shape[0]}")
    print(f"dim_city rows: {dim_city.shape[0]}")
    print(f"dim_sector rows: {dim_sector.shape[0]}")
    print(f"fact_pos_transactions_model rows: {fact_model.shape[0]}")

    print("Data modeling completed successfully.")


if __name__ == "__main__":
    main()