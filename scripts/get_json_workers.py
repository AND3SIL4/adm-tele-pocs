"""
get_json_workers.py

This script provides utilities to extract worker data from a defined Excel table and
return a dictionary with structured information indexed by WorkerId.

Functions:
- get_table_using_range: Loads a specified Excel sheet and table, returning it as a pandas DataFrame.
- get_json_workers: Uses the DataFrame to build a JSON-like dictionary mapping each WorkerId to their details.

Example usage (when run directly):
Reads a table of workers from a config Excel file and prints their info in the designed dict format.
"""

import pandas as pd
from aa_pytools.decorators.safe_execute import safe_execute
from openpyxl import load_workbook


def get_table_using_range(params: dict[str, str]) -> pd.DataFrame:
    """
    Extract a named table from a given Excel file and return as a DataFrame.

    Args:
        params (dict): Must contain "config_file", "sheet_name", and "table_name".

    Returns:
        pd.DataFrame: The table data.
    """
    workbook = load_workbook(filename=params["config_file"], read_only=False)
    worksheet = workbook[params["sheet_name"]]

    # Get the table
    table = worksheet.tables[params["table_name"]]
    table_range = table.ref

    data = worksheet[table_range]
    rows = list(data)
    headers = [cell.value for cell in rows[0]]
    values = [[cell.value for cell in row] for row in rows[1:]]

    return pd.DataFrame(values, columns=headers)


@safe_execute(return_json=True, include_trace=True)
def get_json_workers(params: dict[str, str]) -> str:
    """
    Retrieve worker table as a json indexed by WorkerId, with host and formatted general IDs.

    Args:
        params (dict): Parameters for the Excel read.

    Returns:
        dict: {WorkerId: {"HostId":..., "GeneralId":...}, ...}
    """
    data_frame = get_table_using_range(params=params)
    return {
        row["WorkerId"]: {
            "HostId": row["HostId"],
            "GeneralId": f"{int(row['GeneralId']):03d}",
        }
        for _, row in data_frame.iterrows()
    }


if __name__ == "__main__":
    arguments = {
        "config_file": r"C:\Users\andre\Music\admisiones-tele-config\Configuracion.xlsx",
        "sheet_name": "Listas-blancas",
        "table_name": "WorkersTable",
    }
    print(get_json_workers(arguments))
