import os
import time
from . import state, error_logger
import glob

def get_latest_journal():
    attempts = 0
    while True:
        try:
            time.sleep(8)
            updated_journal_path = glob.glob(os.path.join(state.journal_folder, 'Journal.*.log'))
            if not updated_journal_path:
                print("No journal files found.")
            if updated_journal_path != state.journal_file_path:
                state.new_journal_file = max(updated_journal_path, key=os.path.getctime)
            else:
                continue
            attempts = 0
        except:
            if attempts < 5:
                print("Error reading file. Retrying")
                attempts += 1
            else:
                print("Too many errors. Aborting...")
                time.sleep(2)
                error_logger.log_file_error()
                os._exit(0)