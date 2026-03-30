# dummy_process.py
import time
import signal

PROCESS_NAME = "dummy_rpa_process"

running = True


def stop_process(signum, frame):
    global running
    print(f"[{PROCESS_NAME}] Deteniendo proceso...")
    running = False


signal.signal(signal.SIGINT, stop_process)
signal.signal(signal.SIGTERM, stop_process)


while running:
    time.sleep(5)
