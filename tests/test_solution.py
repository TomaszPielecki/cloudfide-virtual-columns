
import numpy as np
import pandas as pd

from solution import add_virtual_column


def test_original_dataframe_unchanged():
    df = pd.DataFrame({
        "quantity": [2, 3],
        "price": [10, 20]
    })
    original = df.copy(deep=True)

    result = add_virtual_column(df, "quantity * price", "total")

    assert df.equals(original)
    assert result["total"].tolist() == [20, 60]


def test_invalid_column_with_digits():
    df = pd.DataFrame({
        "quantity1": [2],
        "price": [10]
    })

    result = add_virtual_column(df, "quantity1 * price", "total")

    assert result.empty


def test_non_numeric_column():
    df = pd.DataFrame({
        "quantity": ["two", "three"],
        "price": [10, 20]
    })

    result = add_virtual_column(df, "quantity * price", "total")

    assert result.empty


def test_missing_column():
    df = pd.DataFrame({
        "quantity": [2, 3]
    })

    result = add_virtual_column(df, "quantity * price", "total")

    assert result.empty


def test_existing_output_column():
    df = pd.DataFrame({
        "quantity": [2],
        "price": [10],
        "total": [100]
    })

    result = add_virtual_column(df, "quantity * price", "total")

    assert result.empty


def test_float_values():
    df = pd.DataFrame({
        "quantity": [2, 3],
        "price": [10.50, 20.25]
    })

    result = add_virtual_column(df, "quantity * price", "total")

    assert result["total"].tolist() == [21.0, 60.75]


def test_invalid_expression():
    df = pd.DataFrame({
        "quantity": [2],
        "price": [10]
    })

    result = add_virtual_column(
        df,
        "quantity / price",
        "total"
    )

    assert result.empty


def test_underscore_column_names():
    df = pd.DataFrame({
        "unit_price": [10, 20],
        "quantity": [2, 3]
    })

    result = add_virtual_column(
        df,
        "unit_price * quantity",
        "total_revenue"
    )

    assert result["total_revenue"].tolist() == [20, 60]


def test_boolean_values_rejected():
    df = pd.DataFrame({
        "first": [True, False],
        "second": [False, True],
    })

    result = add_virtual_column(
        df,
        "first + second",
        "total"
    )

    assert result.empty


def test_infinite_values_rejected():
    df = pd.DataFrame({
        "first": [1.0, np.inf],
        "second": [2.0, 3.0],
    })

    result = add_virtual_column(
        df,
        "first + second",
        "total"
    )

    assert result.empty


def test_nan_values_rejected():
    df = pd.DataFrame({
        "first": [1.0, np.nan],
        "second": [2.0, 3.0],
    })

    result = add_virtual_column(
        df,
        "first * second",
        "total"
    )

    assert result.empty


def test_infinite_result_rejected():
    df = pd.DataFrame({
        "first": [1e308],
        "second": [1e308],
    })

    result = add_virtual_column(
        df,
        "first * second",
        "total"
    )

    assert result.empty
