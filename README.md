# Virtual Columns and Sales Revenue Pipeline

This repository contains a solution to the Cloudfide recruitment task. It
implements a safe virtual-column function for pandas and uses it in an ETL
pipeline that cleans `sales.csv`, calculates transaction revenue, and writes
regional totals to `revenue_by_region.csv`.

## Requirements

- Python 3.11.9
- Git
- pip
- Quarto CLI (optional, for the HTML report)
- TinyTeX or another LaTeX distribution (optional, for the PDF report)

## Setup

Clone the repository and enter its directory:

```powershell
git clone https://github.com/TomaszPielecki/cloudfide-virtual-columns.git
cd cloudfide-virtual-columns
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the tests

All sample and project tests run with one command:

```powershell
python -m pytest -v
```

## Running the pipeline

```powershell
python pipeline.py
```

The pipeline reads `sales.csv` and writes `revenue_by_region.csv`. Revenue is
calculated in two virtual-column operations:

```text
gross_revenue = quantity * unit_price
revenue = gross_revenue - discount
```

The output contains one row per normalized region and its total revenue,
rounded to two decimal places.

## Data quality issues and handling

The issue counts below were measured after excluding technical rows and exact
duplicates where appropriate. Counts from different cleaning stages are not
additive.

| Problem found | Affected items | Handling |
| --- | ---: | --- |
| Inconsistent source column labels | 7 columns | Strip whitespace, convert to lowercase, and replace spaces with underscores. |
| Repeated header and summary records | 2 rows | Exclude them because they are not transactions. |
| Exact duplicate records | 5 rows | Keep one copy of each record. |
| Missing discounts | 959 rows | Replace missing values with zero. |
| Missing unit prices | 4 rows | Recover each value using the median unit price for the same product. |
| Inconsistent region spelling, case, or whitespace | 15 rows | Strip whitespace and convert names to title case. |
| Quantity values containing whitespace | 4 rows | Remove whitespace before numeric conversion. |
| Unit prices using a decimal comma | 7 rows | Replace the comma with a decimal point before numeric conversion. |
| Negative quantities | 6 rows | Retain them as possible returns or inventory adjustments. |
| Invalid quantities after normalization | 0 rows | Numeric conversion and required-field validation would reject them. |
| Invalid or missing order dates | 0 rows | Parse strictly as `YYYY-MM-DD` and raise `ValueError` if any are invalid. |

After cleaning, 1,500 transaction rows remain.

## Assumptions

- An empty discount means that no discount was applied, so it is treated as
  zero.
- A missing unit price can be recovered from the median known price of the same
  product. The pipeline raises an error if recovery is not possible.
- Negative quantities represent possible returns or inventory adjustments and
  therefore contribute negative revenue instead of being removed.
- Only exact duplicate rows are removed. A repeated order ID alone is not
  sufficient evidence that a transaction is duplicated.
- The discount is a monetary amount deducted from the whole order line, not a
  percentage.
- The source file does not specify a currency, so monetary values are reported
  in dataset units.
- Regional totals are rounded to two decimal places only after aggregation.

## Virtual-column validation

`add_virtual_column()` supports addition, subtraction, and multiplication. It
does not modify its input DataFrame. Invalid expressions, invalid column names,
missing operands, Boolean operands, `NaN`, infinity, or a non-finite result
produce an empty DataFrame.

## Optional report

The analytical report can be generated with Quarto:

```powershell
quarto render reports/sales_analysis.qmd --to html
quarto render reports/sales_analysis.qmd --to pdf
```

Deactivate the virtual environment when finished:

```powershell
deactivate
```
