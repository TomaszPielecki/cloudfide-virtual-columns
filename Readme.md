## Environment Setup

### Requirements

- Python 3.11.9
- Git
- pip
- Quarto CLI (optional, for HTML/PDF reports)
- TinyTeX or another LaTeX distribution (optional, for PDF reports)

### 1. Clone the repository

```powershell
git clone https://github.com/TomaszPielecki/cloudfide-virtual-columns.git
cd cloudfide-virtual-columns
```

### 2. Select Python 3.11.9

If using pyenv-win:

```powershell
pyenv install 3.11.9
pyenv local 3.11.9
python --version
```

The `pyenv install` command can be skipped if Python 3.11.9 is already installed.

Alternatively, use an existing Python 3.11.9 installation.

### 3. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Run the tests

```powershell
python -m pytest -v
```

### 6. Run the ETL pipeline

```powershell
python pipeline.py
```

The pipeline reads `sales.csv`, cleans the data, calculates revenue using the custom `add_virtual_column()` function, and generates `revenue_by_region.csv`.

### 7. Generate reports (optional)

Install Quarto CLI separately and configure a LaTeX distribution for PDF output.

```powershell
quarto render reports/sales_analysis.qmd --to html
quarto render reports/sales_analysis.qmd --to pdf
```

### 8. Deactivate the virtual environment

```powershell
deactivate
```