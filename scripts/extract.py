import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("/opt/airflow/project/data/raw")
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

DATASET_URL = (
    "https://data.kapsarc.org/api/explore/v2.1/catalog/datasets/"
    "point-of-sale-transactions-by-sector-and-city/exports/csv"
    "?lang=en&timezone=Asia%2FRiyadh&use_labels=true&delimiter=%2C"
)

OUTPUT_FILE = RAW_DATA_PATH / "saudi_pos_raw.csv"


def main():
    print("Starting data extraction...")
    print(f"Downloading data from: {DATASET_URL}")

    df = pd.read_csv(DATASET_URL)

    print(f"Rows extracted: {df.shape[0]}")
    print(f"Columns extracted: {df.shape[1]}")
    print("Columns:")
    print(df.columns.tolist())

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Raw data saved to: {OUTPUT_FILE}")
    print("Extraction completed successfully.")


if __name__ == "__main__":
    main()