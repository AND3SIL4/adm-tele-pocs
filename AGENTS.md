# AGENTS.md - Agent Coding Guidelines for adm-tele-poc

## Project Overview

Python project (>=3.13) for processing Excel files related to medical teleorientation appointments. Uses pandas and openpyxl for data processing, integrates with Automation Anywhere via aa-pytools.

## Build / Lint / Test Commands

### Running the Application

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run scripts
python scripts/extraction_transform_load.py
python scripts/get_json_workers.py
python scripts/balancer_round_robin.py
python scripts/update_final_file.py
```

### Linting

```bash
# Run ruff linter
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format code
ruff format .
```

### Testing

No tests currently exist. To add tests:

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_file_name.py

# Run a single test function
pytest tests/test_file_name.py::test_function_name

# Run tests matching a pattern
pytest -k "test_pattern"
```

## Code Style Guidelines

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `ETLInputFile`, `BalancerRowRun` |
| Functions/variables | snake_case | `etl_file`, `file_path`, `path_files` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Private methods | Prefix with underscore | `_read_file`, `_filter_specialization` |

### Import Organization

```python
# Standard library
import pandas as pd

# Third-party libraries
from aa_pytools.decorators.safe_execute import safe_execute
from openpyxl import load_workbook
```

Order: Standard library → Third-party → Project local. Separate groups with blank line.

### Type Hints

Always use type hints:

```python
def __init__(self, file_path: str, keyword: str, date_to_filter: str) -> None:
def _read_file(self, file_path: str) -> pd.DataFrame:
def extract_transform_load(self) -> dict:
```

### Docstrings

Use Google-style docstrings:

```python
def get_table_using_range(params: dict[str, str]) -> pd.DataFrame:
    """
    Extract a named table from a given Excel file and return as a DataFrame.

    Args:
        params (dict): Must contain "config_file", "sheet_name", and "table_name".

    Returns:
        pd.DataFrame: The table data.
    """
```

### Error Handling

Use `@safe_execute` decorator for Automation Anywhere integration:

```python
@safe_execute(return_json=True, include_trace=True)
def get_json_workers(params: dict[str, str]) -> str:
    # Function logic here
```

### Class Structure

```python
class ETLInputFile:
    def __init__(self, file_path: str, keyword: str, date_to_filter: str) -> None:
        self.file_path = file_path
        self.keyword_to_filter = keyword
        self.date_filter = date_to_filter

    def _private_method(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        pass

    def public_method(self) -> dict:
        pass
```

### File Organization

- Scripts go in `scripts/` directory
- Descriptive names: `extraction_transform_load.py`, `get_json_workers.py`, `balancer_round_robin.py`, `update_final_file.py`
- One class or main purpose per file

### Excel Operations

- Always use `engine="openpyxl"` when reading Excel files
- Use `pd.to_datetime()` with `dayfirst=True` for Spanish dates (DD/MM/YYYY)
- Handle NaN with `na=False` in string operations

### Best Practices

1. Use `.copy()` when modifying DataFrames to avoid SettingWithCopyWarning
2. Prefer method chaining for DataFrame operations
3. Extract magic numbers as constants
4. Use early returns to reduce nesting
5. Single responsibility: each function does one thing

## Dependencies

- `aa-pytools>=1.0.0` - Automation Anywhere tools
- `openpyxl>=3.1.5` - Excel file handling
- `pandas>=3.0.1` - Data processing

## Common Tasks

**Running ETL pipeline:**
```python
params = {
    "file_path": r"path\to\file.xlsx",
    "date_to_filter": "02/03/2026",
    "keyword": "teleorientacion",
}
result = etl_file(incomes=params)
```

**Reading Excel tables with named ranges:**
```python
arguments = {
    "config_file": r"path\to\Configuracion.xlsx",
    "sheet_name": "Listas-blancas",
    "table_name": "WorkersTable",
}
workers = get_json_workers(arguments)
```

## Important Notes

- Project processes medical appointment data - handle with appropriate confidentiality
- Excel files contain Spanish column names (e.g., "Nombre de la especialidad / procedimiento", "Estado de la cita")
- Date format in source files is DD/MM/YYYY
