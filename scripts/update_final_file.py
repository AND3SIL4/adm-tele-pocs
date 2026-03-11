import pandas as pd
from aa_pytools.decorators.safe_execute import safe_execute


class UpdateFinalFile:
    """Handles updating a final Excel file by appending data from a temporary CSV file."""

    def __init__(self, file_path: str, sheet_name: str, temp_file: str) -> None:
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.temp_file = temp_file

    def _read_file(self, file_path: str, sheet_name: str | None = None) -> pd.DataFrame:
        if file_path.lower().endswith(".csv"):
            return pd.read_csv(file_path, delimiter=",")
        if sheet_name is None:
            raise ValueError("sheet_name is required for Excel files")
        return pd.read_excel(io=file_path, sheet_name=sheet_name, engine="openpyxl")

    def _save_file(self, dataframes: list[pd.DataFrame]) -> None:
        final_df = pd.concat(dataframes, ignore_index=True)
        final_df.to_excel(self.file_path, sheet_name=self.sheet_name, index=False)

    def update_final_file(self) -> None:
        temp_df = self._read_file(self.temp_file)
        existing_df = self._read_file(self.file_path, sheet_name=self.sheet_name)
        self._save_file([existing_df, temp_df])


@safe_execute
def update_final_file(params: dict[str, str]) -> str:
    update_final = UpdateFinalFile(**params)
    update_final.update_final_file()


if __name__ == "__main__":
    arguments = {
        "file_path": r"C:\dev-projects\adm-tele-poc\outputs\test-test.xlsx",
        "sheet_name": "pacientes-con-cita",
        "temp_file": r"C:\dev-projects\adm-tele-poc\outputs\temp.csv",
    }
    print(update_final_file(params=arguments))
