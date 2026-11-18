
import pandas as pd
import pytest

from pipeline import (
    load_sales,
    clean_sales,
    calculate_revenue,
    aggregate_revenue,
)


def test_load_sales():
    """Verify the number of rows after initial cleaning."""
    df = load_sales()

    assert len(df) == 1500
    assert df.duplicated().sum() == 0


def test_clean_sales():
    """Verify data cleaning and missing values."""
    df = clean_sales(load_sales())

    assert len(df) == 1500
    assert df["discount"].isna().sum() == 0
    assert df["unit_price"].isna().sum() == 0
    assert df["quantity"].isna().sum() == 0


def test_regions():
    """Verify normalized region names."""
    df = clean_sales(load_sales())

    expected = {
        "North", "South", "East",
        "West", "Central"
    }

    assert set(df["region"]) == expected


def test_revenue_calculation():
    """Check revenue calculation on sample data."""
    df = pd.DataFrame({
        "quantity": [2, 3],
        "unit_price": [100.0, 50.0],
        "discount": [10.0, 0.0]
    })

    result = calculate_revenue(df)

    assert result["revenue"].tolist() == [190.0, 150.0]


def test_revenue_aggregation():
    """Verify grouping and total revenue."""
    df = pd.DataFrame({
        "region": ["North", "South", "North"],
        "revenue": [100.0, 200.0, 50.0]
    })

    result = aggregate_revenue(df)

    totals = dict(zip(result["region"], result["revenue"]))

    assert totals["North"] == pytest.approx(150.0)
    assert totals["South"] == pytest.approx(200.0)


def test_total_revenue_consistency():
    """Aggregated revenue must equal transaction revenue."""
    df = calculate_revenue(clean_sales(load_sales()))
    result = aggregate_revenue(df)

    assert result["revenue"].sum() == pytest.approx(
        df["revenue"].sum(),
        abs=0.01
    )

def test_invalid_order_date():
    """Pipeline must reject invalid order dates."""

    df = load_sales()

    df.loc[0, "order_date"] = "not-a-date"

    with pytest.raises(
        ValueError,
        match="Invalid or missing order dates"
    ):
        clean_sales(df)

def test_impossible_order_date():
    """Pipeline must reject impossible dates."""

    df = load_sales()

    df.loc[0, "order_date"] = "2026-02-30"

    with pytest.raises(
        ValueError,
        match="Invalid or missing order dates"
    ):
        clean_sales(df)    
