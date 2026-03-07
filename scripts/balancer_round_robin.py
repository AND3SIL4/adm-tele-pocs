import os

import pandas as pd
from aa_pytools.decorators.safe_execute import safe_execute


# Class to distribute rows among workers for parallel processing
class BalancerRowRun:
    def __init__(
        self,
        file_path: str,
        sheet_name: str,
        file_server: str,
        active_workers: dict[str, str],
    ) -> None:
        self.file_path = file_path
        self.file_server = file_server
        self.active_workers = active_workers
        self.sheet_name = sheet_name

        self._validate_intputs()  # Simple input validations

    def _validate_intputs(self) -> None:
        # Check if file exists
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {self.file_path}")

        # Ensure there is at least one worker
        if len(self.active_workers) <= 0:
            raise ValueError(
                "No se han encontrado máquinas activas para hacer la distribución"
            )

    def _read_file(self, file_path: str, sheet_name: str) -> pd.DataFrame:
        # Read the Excel file with openpyxl engine
        return pd.read_excel(io=file_path, engine="openpyxl", sheet_name=sheet_name)

    def _save_file(
        self, data_frame: pd.DataFrame, final_file: str, sheet_name: str
    ) -> None:
        # Save the DataFrame to Excel
        data_frame.to_excel(excel_writer=final_file, sheet_name=sheet_name)

    def _split_round_robin(
        self, data_frame: pd.DataFrame, workers: int
    ) -> list[pd.DataFrame]:
        # Split records into chunks for each worker using round robin
        chunks: list[pd.DataFrame] = []
        for i in range(workers):
            chunk = data_frame.iloc[i::workers]
            chunks.append(chunk)
        return chunks

    def balance_records(self) -> dict:
        """
        Distribute the DataFrame rows evenly to each worker.
        Each worker receives roughly same amount, round robin.
        Results and file locations returned in a dict.
        """
        total_workers = len(self.active_workers)
        origin_df = self._read_file(self.file_path, self.sheet_name)

        if total_workers == 1:
            # Only one worker: write whole file
            keyworker: dict[str] = next(iter(self.active_workers))
            dic_keyworker = self.active_workers.get(keyworker)
            if not dic_keyworker:
                raise ValueError("Error accediendo a la información de la máquina")
            name_file = f"{keyworker}-{dic_keyworker.get('HostId')}-{self.sheet_name}"
            final_path = f"{self.file_server}/{name_file}.xlsx"
            self._save_file(origin_df, final_path, self.sheet_name)
            return {keyworker: {"file": final_path, "records": len(origin_df)}}

        # More than one worker: split file
        chunks_splited = self._split_round_robin(origin_df, total_workers)

        # Assign splits to each worker
        worker_keys = list(self.active_workers.keys())
        assignment_results = {}
        for idx, worker_key in enumerate(worker_keys):
            worker_info = self.active_workers[worker_key]
            chunk = chunks_splited[idx] if idx < len(chunks_splited) else None
            if chunk is not None and not chunk.empty:
                # Compose filename for this worker
                name_file = (
                    f"{worker_key}-{worker_info.get('HostId')}-{self.sheet_name}"
                )
                final_path = f"{self.file_server}/{name_file}.xlsx"
                # Write worker's assigned rows to file
                self._save_file(chunk, final_path, self.sheet_name)
                assignment_results[worker_key] = {
                    "file": final_path,
                    "records": len(chunk),
                }
            else:
                # Worker gets no records
                assignment_results[worker_key] = {"file": None, "records": 0}

        return assignment_results  # Return results for all workers


# Automation Anywhere integration: entry function
@safe_execute(return_json=True, include_trace=True)
def balance_row_run(params: dict) -> str:
    # Create and run the balance
    balancer = BalancerRowRun(**params)
    return balancer.balance_records()


# Example usage
if __name__ == "__main__":
    arguments = {
        "file_path": r"C:\dev-projects\adm-tele-poc\public\admisiones-teleorientaciton-con-cita.xlsx",
        "sheet_name": "pacientes-con-cita",
        "file_server": r"C:\dev-projects\adm-tele-poc\outputs",
        "active_workers": {
            "npco11xh3010afsilva": {"HostId": "srvvpkrpacli01", "GeneralId": "001"},
            "other_worker": {"HostId": "srvvpkrpacli01", "GeneralId": "001"},
        },
    }
    print(balance_row_run(params=arguments))
