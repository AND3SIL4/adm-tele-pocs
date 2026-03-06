# Script to process and filter medical teleorientation appointment Excel files
# Loads data, filters by specialization, appointment state, and date,
# sorts by appointment time, and writes results to Excel.

import os

import pandas as pd
from aa_pytools.decorators.safe_execute import safe_execute


class ETLInputFile:
    # List of required columns in the input Excel file
    _required_cols = [
        "Nombre de la especialidad / procedimiento",
        "Estado de la cita",
        "Fecha de la Cita",
        "Hora de la Cita",
        "Nombre de la sede",
    ]

    def __init__(
        self,
        file_path: str,
        keyword: str,
        date_to_filter: str,
        final_file: str,
        sheet_name: str,
    ) -> None:
        # file_path: path to the Excel file
        # keyword: text to search in the specialization column
        # date_to_filter: appointment date (string, format DD/MM/YYYY)
        self.file_path = file_path
        self.keyword_to_filter = keyword
        self.date_filter = date_to_filter
        self.final_file = final_file
        self.sheet_name = sheet_name

    def _validate_input(self) -> None:
        # Check if file exists and all required columns exist
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

        data_frame = self._read_file(file_path=self.file_path)
        missing = set(self._required_cols) - set(data_frame.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    def _read_file(self, file_path: str) -> pd.DataFrame:
        # Read Excel file using openpyxl
        return pd.read_excel(
            io=file_path, engine="openpyxl", sheet_name=self.sheet_name
        )

    def _filter_specialization(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        # Filter rows by specialization keyword (case-insensitive, ignore NaN)
        return data_frame[
            data_frame["Nombre de la especialidad / procedimiento"]
            .astype(str)
            .str.contains(self.keyword_to_filter, case=False, na=False)
        ]

    def _filter_appointment_state(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        # Filter rows where appointment state is 'pendiente'
        return data_frame[
            data_frame["Estado de la cita"].astype(str).str.lower() == "pendiente"
        ]

    def _filter_by_date(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        # Filter rows by appointment date
        data_frame = data_frame.copy()
        data_frame["Fecha de la Cita"] = pd.to_datetime(
            data_frame["Fecha de la Cita"], dayfirst=True
        )
        return data_frame[
            data_frame["Fecha de la Cita"].dt.date
            == pd.to_datetime(self.date_filter).date()
        ]

    def _filter_file(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        # Apply all filters in sequence
        data_frame = self._filter_specialization(data_frame)
        data_frame = self._filter_appointment_state(data_frame)
        data_frame = self._filter_by_date(data_frame)
        return data_frame

    def _sort_record_by_appoitment_and_branch(
        self, data_frame: pd.DataFrame
    ) -> pd.DataFrame:
        # Sort by appointment hour priority (earliest first)
        data_frame = data_frame.copy()
        data_frame["Hora de la Cita"] = pd.to_datetime(
            data_frame["Hora de la Cita"], format="%H:%M:%S", errors="coerce"
        ).dt.time
        sorted_df = data_frame.sort_values(
            by=["Hora de la Cita", "Nombre de la sede"], ascending=True
        )
        return sorted_df

    def _save_excel_file(self, data_frame: pd.DataFrame) -> None:
        data_frame.to_excel(
            excel_writer=self.final_file, index=False, sheet_name=self.sheet_name
        )

    def extract_transform_load(self) -> dict:
        # Main ETL process: read, filter, sort, output, and return info
        origin_df: pd.DataFrame = self._read_file(file_path=self.file_path)
        filtered_df: pd.DataFrame = self._filter_file(data_frame=origin_df)
        filtered_df = self._sort_record_by_appoitment_and_branch(filtered_df)
        self._save_excel_file(data_frame=filtered_df)  # Save to the final file
        # Return record counts
        return {"original_length": len(origin_df), "real_length": len(filtered_df)}


@safe_execute(return_json=True, include_trace=True)
def etl_file(incomes: dict[str, str]) -> str:
    # Wrapper for ETL process for Automation Anywhere integration
    etl_input_file: ETLInputFile = ETLInputFile(**incomes)
    insights: dict = etl_input_file.extract_transform_load()
    return insights


if __name__ == "__main__":
    # Example usage demonstration
    params = {
        "file_path": r"C:\dev-projects\adm-tele-poc\public\admisiones-teleorientaciton-con-cita.xlsx",
        "date_to_filter": "02/03/2026",
        "keyword": "teleorientacion",
        "sheet_name": "pacientes-con-cita",
        "final_file": r"test.xlsx",
    }
    print(etl_file(incomes=params))
