import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("/opt/airflow/project/data/raw")
PROCESSED_DATA_PATH = Path("/opt/airflow/project/data/processed")

INPUT_FILE = RAW_DATA_PATH / "saudi_pos_raw.csv"
OUTPUT_FILE = PROCESSED_DATA_PATH / "fact_pos_transactions.csv"


def clean_column_names(df):
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("%", "pct", regex=False)
    )
    return df


def main():
    print("Starting transformation...")

    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_FILE)

    print(f"Raw rows: {df.shape[0]}")
    print(f"Raw columns: {df.shape[1]}")

    df = clean_column_names(df)

    # Rename columns to simpler names
    df = df.rename(
        columns={
            "starting_date": "date",
            "sectors": "sector",
            "value_multiple_units": "value"
        }
    )

    # Convert date
    df["date"] = pd.to_datetime(df["date"])

    # Keep only the main numeric indicators
    main_indicators = [
        "Number of Transactions (In Thousand)",
        "Value of Transactions (In Thousand SAR)"
    ]

    df = df[df["indicator"].isin(main_indicators)].copy()

    # Pivot indicator values into separate columns
    fact_pos = df.pivot_table(
        index=["date", "city", "sector"],
        columns="indicator",
        values="value",
        aggfunc="sum"
    ).reset_index()

    # Flatten column names
    fact_pos.columns.name = None

    fact_pos = fact_pos.rename(
        columns={
            "Number of Transactions (In Thousand)": "transaction_count_thousand",
            "Value of Transactions (In Thousand SAR)": "transaction_value_thousand_sar"
        }
    )

    # Calculate average transaction value in SAR
    fact_pos["avg_transaction_value_sar"] = (
        fact_pos["transaction_value_thousand_sar"] /
        fact_pos["transaction_count_thousand"]
    )

    # Replace infinite values if division issue happens
    fact_pos["avg_transaction_value_sar"] = (
        fact_pos["avg_transaction_value_sar"]
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )

    # Sort data
    fact_pos = fact_pos.sort_values(["date", "city", "sector"])

    fact_pos.to_csv(OUTPUT_FILE, index=False)

    print(f"Processed rows: {fact_pos.shape[0]}")
    print(f"Processed columns: {fact_pos.shape[1]}")
    print("Processed columns:")
    print(fact_pos.columns.tolist())
    print(f"Processed data saved to: {OUTPUT_FILE}")
    print("Transformation completed successfully.")


if __name__ == "__main__":
    main()