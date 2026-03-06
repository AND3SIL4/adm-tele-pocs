import os

import pandas as pd
from aa_pytools.decorators.safe_execute import safe_execute


# Apply OOP to manage the reusable rules
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

        self._validate_intputs()  # Validate the inputs

    def _validate_intputs(self) -> None:
        # File existing
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {self.file_path}")

        # Validate total workers
        if len(self.active_workers) <= 0:
            raise ValueError(
                "No se han encontrado máquinas activas para hacer la distribución"
            )

    def _read_file(self, file_path: str, sheet_name: str) -> pd.DataFrame:
        return pd.read_excel(io=file_path, engine="openpyxl", sheet_name=sheet_name)

    def _save_file(
        self, data_frame: pd.DataFrame, final_file: str, sheet_name: str
    ) -> None:
        data_frame.to_excel(excel_writer=final_file, sheet_name=sheet_name)

    def _split_round_robin(
        self, data_frame: pd.DataFrame, workers: int
    ) -> list[pd.DataFrame]:
        chunks: list[pd.DataFrame] = []
        for i in range(workers):
            # Slicing [inicio:fin:paso]
            # Takes the firs row until the end and increments by total workers
            chunk = data_frame.iloc[i::workers]
            chunks.append(chunk)

        return chunks

    def balance_records(self) -> dict:
        # To balance total records we use the Round Robin type
        # This type of balancer allows to dive the amount of records equity
        # Assign workload row by row to avoid more stress in only one worker
        total_workers = len(self.active_workers)
        origin_df = self._read_file(self.file_path, self.sheet_name)

        if total_workers == 1:
            keyworker: dict[str] = next(iter(self.active_workers))
            dic_keyworker = self.active_workers.get(keyworker)

            if not dic_keyworker:
                raise ValueError("Error accediendo a la información de la máquina")

            name_file = f"{keyworker}-{dic_keyworker.get('HostId')}-{self.sheet_name}"
            final_path = f"{self.file_server}/{name_file}.xlsx"

            # Save the only file and stop another activities
            self._save_file(origin_df, final_path, self.sheet_name)
            return {"total_balanced": total_workers}

        chunks_splited = self._split_round_robin(origin_df, total_workers)

        # Assign each split chunk to one active worker in the order of keys
        # Matching chunk index to worker: chunk 0 -> worker 0, chunk 1 -> worker 1, etc.
        worker_keys = list(self.active_workers.keys())
        assignment_results = {}

        for idx, worker_key in enumerate(worker_keys):
            worker_info = self.active_workers[worker_key]
            chunk = chunks_splited[idx] if idx < len(chunks_splited) else None

            if chunk is not None and not chunk.empty:
                # Build filename using worker key, HostId, and sheet name
                name_file = (
                    f"{worker_key}-{worker_info.get('HostId')}-{self.sheet_name}"
                )
                final_path = f"{self.file_server}/{name_file}.xlsx"

                # Save the assigned chunk for each worker
                self._save_file(chunk, final_path, self.sheet_name)
                assignment_results[worker_key] = {
                    "file": final_path,
                    "records": len(chunk),
                }
            else:
                assignment_results[worker_key] = {"file": None, "records": 0}

        return assignment_results  # Metrics and insights needed


# Apply function to integrate at Automation Anywhere Control Room
@safe_execute(return_json=True, include_trace=True)
def balance_row_run(params: dict) -> str:
    balancer = BalancerRowRun(**params)
    return balancer.balance_records()


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
