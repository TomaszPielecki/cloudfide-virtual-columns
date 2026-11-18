from pathlib import Path

import pandas as pd
from solution import add_virtual_column


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sales.csv"
OUTPUT_FILE = BASE_DIR / "revenue_by_region.csv"


def load_sales() -> pd.DataFrame:
    """Load and initially clean the sales dataset."""

    # 1. Read raw data
    df = pd.read_csv(INPUT_FILE, dtype="string")

    # 2. Normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print(f"Loaded rows: {len(df)}")

    # 3. Remove repeated header and summary row
    technical_rows = df["order_id"].isin(
        ["Order ID", "TOTAL"]
    )

    print(f"Technical rows: {technical_rows.sum()}")

    df = df.loc[~technical_rows].copy()

    # 4. Remove exact duplicates
    duplicate_count = df.duplicated().sum()

    print(f"Duplicate rows: {duplicate_count}")

    df = df.drop_duplicates().reset_index(drop=True)

    print(f"Rows after initial cleaning: {len(df)}")

    return df


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Clean sales data and prepare it for calculations."""

    df = df.copy()

    # 1. Normalize text values
    df["region"] = df["region"].str.strip().str.title()
    df["product"] = df["product"].str.strip()

    # 2. Convert numeric columns
    numeric_columns = [
        "quantity",
        "unit_price",
        "discount"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column]
            .str.strip()
            .str.replace(" ", "", regex=False)
            .str.replace(",", ".", regex=False),
            errors="coerce"
        )

    # 3. Replace missing discounts with zero
    missing_discounts = df["discount"].isna().sum()

    df["discount"] = df["discount"].fillna(0)

    # 4. Recover missing unit prices using product prices
    missing_prices = df["unit_price"].isna().sum()

    product_prices = (
        df.groupby("product")["unit_price"]
        .median()
    )

    df["unit_price"] = df["unit_price"].fillna(
        df["product"].map(product_prices)
    )

    # 5. Validate required fields
    required_columns = [
        "order_id",
        "region",
        "product",
        "quantity",
        "unit_price",
        "order_date"
    ]

    if df[required_columns].isna().any().any():
        raise ValueError(
            "Missing required sales data after cleaning"
        )

    # 6. Display cleaning summary
    print(f"Missing discounts filled: {missing_discounts}")
    print(f"Missing prices recovered: {missing_prices}")
    print(
        "Remaining missing prices:",
        df["unit_price"].isna().sum()
    )
    print(f"Cleaned rows: {len(df)}")

    return df

def calculate_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate revenue using virtual columns."""

    # Calculate gross revenue
    df = add_virtual_column(
        df,
        "quantity * unit_price",
        "gross_revenue"
    )

    if df.empty:
        raise ValueError("Failed to calculate gross revenue")

    # Subtract discounts
    df = add_virtual_column(
        df,
        "gross_revenue - discount",
        "revenue"
    )

    if df.empty:
        raise ValueError("Failed to calculate net revenue")

    print("\n=== REVENUE CALCULATION ===")
    print(df[[
        "quantity",
        "unit_price",
        "discount",
        "gross_revenue",
        "revenue"
    ]].head(10).to_string(index=False))

    return df


def aggregate_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total revenue by region."""

    result = (
        df.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("region")
        .reset_index(drop=True)
    )

    # Round monetary totals to two decimal places
    result["revenue"] = result["revenue"].round(2)

    return result




def main():
    """Run the complete sales ETL pipeline."""

    print("\n=== CLOUDFIDE SALES ETL ===")

    # Extract
    sales = load_sales()

    # Transform
    sales = clean_sales(sales)

    # Calculate revenue
    sales = calculate_revenue(sales)

    # Aggregate
    revenue_by_region = aggregate_revenue(sales)

    # Load / Export
    revenue_by_region.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n=== REVENUE BY REGION ===")
    print(revenue_by_region.to_string(index=False))

    print(f"\nOutput saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
