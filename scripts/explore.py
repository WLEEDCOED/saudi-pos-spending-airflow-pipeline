import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("/opt/airflow/project/data/raw")
INPUT_FILE = RAW_DATA_PATH / "saudi_pos_raw.csv"


def main():
    df = pd.read_csv(INPUT_FILE)

    print("Dataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 10 rows:")
    print(df.head(10))

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nUnique values per column:")
    for column in df.columns:
        print(f"{column}: {df[column].nunique()} unique values")

    print("\nSample indicators:")
    print(df["Indicator"].dropna().unique()[:20])

    print("\nSample sectors:")
    print(df["Sectors"].dropna().unique()[:20])

    print("\nSample cities:")
    print(df["City"].dropna().unique()[:20])


if __name__ == "__main__":
    main()