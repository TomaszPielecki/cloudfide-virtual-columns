
import operator
import re

import pandas as pd
from pandas.api.types import is_numeric_dtype


def add_virtual_column(
    df: pd.DataFrame,
    role: str,
    new_column: str
) -> pd.DataFrame:

    # 1. Validate input arguments
    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame()

    if not isinstance(role, str) or not isinstance(new_column, str):
        return pd.DataFrame()

    # 2. Validate column names
    label_pattern = r"[A-Za-z_]+"

    if not re.fullmatch(label_pattern, new_column):
        return pd.DataFrame()

    if any(
        not isinstance(col, str)
        or not re.fullmatch(label_pattern, col)
        for col in df.columns
    ):
        return pd.DataFrame()

    if new_column in df.columns:
        return pd.DataFrame()

    # 3. Parse the mathematical expression
    expression_pattern = (
        r"\s*([A-Za-z_]+)\s*([+*-])\s*([A-Za-z_]+)\s*"
    )

    match = re.fullmatch(expression_pattern, role)

    if match is None:
        return pd.DataFrame()

    left_column, operation, right_column = match.groups()

    # 4. Check that both columns exist
    if left_column not in df.columns or right_column not in df.columns:
        return pd.DataFrame()

    # 5. Validate numeric data types
    if not is_numeric_dtype(df[left_column]):
        return pd.DataFrame()

    if not is_numeric_dtype(df[right_column]):
        return pd.DataFrame()

    # 6. Define supported operations
    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
    }

    # 7. Create a new DataFrame
    result = df.copy()

    try:
        result[new_column] = operations[operation](
            df[left_column],
            df[right_column]
        )
    except (TypeError, ValueError, ArithmeticError):
        return pd.DataFrame()

    return result
