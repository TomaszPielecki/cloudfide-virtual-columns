
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_DIR / "sales.csv"


def main():
    df = pd.read_csv(CSV_PATH)

    print("\n=== DATASET OVERVIEW ===")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("\n=== COLUMN NAMES ===")
    for column in df.columns:
        print(repr(column))

    print("\n=== DATA TYPES ===")
    print(df.dtypes)

    print("\n=== MISSING VALUES ===")
    print(df.isna().sum())

    print("\n=== DUPLICATED ROWS ===")
    print(df.duplicated().sum())

    print("\n=== REGION VALUES ===")
    print(df["Region"].value_counts(dropna=False))

    print("\n=== FIRST 10 RECORDS ===")
    print(df.head(10).to_string(index=False))

    print("\n=== NUMERIC COLUMN CHECK ===")
    for column in ["Quantity ", "Unit Price", "Discount"]:
        values = pd.to_numeric(
            df[column].astype("string").str.strip()
                .str.replace(",", ".", regex=False),
            errors="coerce"
        )

        invalid = df[column].notna() & values.isna()

        print(f"{column!r}: {invalid.sum()} invalid values")


if __name__ == "__main__":
    main()
