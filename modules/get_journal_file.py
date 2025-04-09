import os
import time
from . import state
import glob

def get_latest_journal():
    attempts = 0
    while True:
        try:
            time.sleep(8)
            state.new_journal_file = glob.glob(os.path.join(state.journal_folder, 'Journal.*.log'))
            if not state.new_journal_file:
                print("No journal files found.")
            if state.new_journal_file != state.journal_file_path:
                state.new_journal_file = max(state.new_journal_file, key=os.path.getctime)
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
                os._exit(0)