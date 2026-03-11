import pandas as pd
from aa_pytools.decorators.safe_execute import safe_execute


# Class for updating an Excel file by appending rows from a temporary CSV file
class UpdateFinalFile:
    """Handles updating a final Excel file by appending data from a temporary CSV file."""

    def __init__(self, file_path: str, sheet_name: str, temp_file: str) -> None:
        # Save file path, sheet name, and path to temp CSV file as instance variables
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.temp_file = temp_file

    # Internal method to read a file (CSV or Excel), returning a pandas DataFrame
    def _read_file(self, file_path: str, sheet_name: str | None = None) -> pd.DataFrame:
        if file_path.lower().endswith(".csv"):
            # Read CSV file with comma delimiter
            return pd.read_csv(file_path, delimiter=",")
        if sheet_name is None:
            # Raise error if sheet name missing for Excel files
            raise ValueError("sheet_name is required for Excel files")
        # Read Excel file using specified sheet and openpyxl engine
        return pd.read_excel(file_path, sheet_name, engine="openpyxl")

    # Save merged DataFrames to the target Excel file
    def _save_file(self, dataframes: list[pd.DataFrame]) -> None:
        # Concatenate given DataFrames, reset index, and save to Excel
        final_df = pd.concat(dataframes, ignore_index=True)
        final_df.to_excel(self.file_path, sheet_name=self.sheet_name, index=False)

    # Main method to update the final Excel file by appending temp CSV data
    def update_final_file(self) -> None:
        # Read temporary data from CSV
        temp_df = self._read_file(self.temp_file)
        print(temp_df)
        # Read existing data from final Excel file
        existing_df = self._read_file(self.file_path, sheet_name=self.sheet_name)
        print(existing_df)
        # Combine both and save result to Excel
        self._save_file([existing_df, temp_df])


@safe_execute
def update_final_file(params: dict[str, str]) -> str:
    # Entrypoint for Automation Anywhere – expects params dict:
    # {
    #   "file_path": <Excel path>,
    #   "sheet_name": <Sheet name>,
    #   "temp_file": <Temp CSV path>
    # }
    update_final = UpdateFinalFile(**params)
    update_final.update_final_file()


if __name__ == "__main__":
    # Example usage: run this script directly for manual testing
    arguments = {
        "file_path": r"C:\dev-projects\adm-tele-poc\outputs\test-test.xlsx",
        "sheet_name": "pacientes-con-cita",
        "temp_file": r"C:\dev-projects\adm-tele-poc\outputs\temp.csv",
    }
    print(update_final_file(params=arguments))
