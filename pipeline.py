
from pathlib import Path

import pandas as pd

from solution import add_virtual_column


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sales.csv"
OUTPUT_FILE = BASE_DIR / "revenue_by_region.csv"


def load_sales() -> pd.DataFrame:
    """Load and prepare the raw sales dataset."""

    df = pd.read_csv(INPUT_FILE, dtype="string")

    # Normalize column labels
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print(f"Loaded rows: {len(df)}")

    # Remove repeated header and summary row
    technical_rows = df["order_id"].isin(
        ["Order ID", "TOTAL"]
    )

    print(f"Technical rows: {technical_rows.sum()}")

    df = df.loc[~technical_rows].copy()

    # Remove exact duplicates
    duplicate_count = df.duplicated().sum()

    print(f"Duplicate rows: {duplicate_count}")

    df = df.drop_duplicates().reset_index(drop=True)

    print(f"Rows after initial cleaning: {len(df)}")

    return df


if __name__ == "__main__":
    sales = load_sales()
    print(sales.head())
