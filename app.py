import os
import time
import configparser
import json
import threading
import glob
from modules import state, journal_logging, exit_app, select_app_mode, shopping_list, clean_screen, del_tracking_again, get_journal_file, error_logger, delivery_tracking

def get_latest_journal():
    latest_file = glob.glob(os.path.join(state.journal_folder, 'Journal.*.log'))
    if not latest_file:
        print("No journal files found.")
    newest_file = max(latest_file, key=os.path.getctime)
    return newest_file

def main_loop():
    try:
        with open(state.journal_file_path) as f:
            f.seek(0, os.SEEK_END)
            while True:
                if state.journal_file_path != state.new_journal_file:
                    state.journal_file_path = state.new_journal_file
                    return main_loop()
                state.lines = f.readlines()
                if not state.lines and state.just_started == False and state.switched != True:
                    time.sleep(0.5)
                else:
                    if state.app_mode == "3":
                        state.just_started = False
                        journal_logging.log_mode()
                    elif state.app_mode == "2":
                        state.just_started = False
                        shopping_list.tracking_mode()
                    elif state.app_mode == "1":
                        state.just_started = False
                        #del_tracking_again.colonisation_tracker()
                        delivery_tracking.colonisation_tracker()
                        time.sleep(0.3)
    except json.JSONDecodeError:
        print(f"Json decode error")

def start():
    try:
        clean_screen.clear_screen()
        print(f'ED Construction helper {state.current_version} \n Type "help" for a list of commands')
        config = configparser.ConfigParser()
        config.read('config.ini')
        config.sections()
        file_check_thread = False
        state.journal_folder
        state.journal_folder = config['JOURNAL_PATH']['path']
        state.journal_file_path = get_latest_journal()
        if state.journal_file_path == "None":
            print("No journal files found. Exiting...")
            time.sleep(1)
            exit_app.close_app()
        if not state.journal_file_path:
            print("No journal files found.")
            time.sleep(1)
            exit_app.close_app()
        state.new_journal_file = state.journal_file_path
        select_app_mode.app_mode_selection()
        state.ship_cargo_space = 0
        file_check_thread = threading.Thread(target=get_journal_file.get_latest_journal, daemon=True)
        file_check_thread.start()
        main_loop()
    except:
        error_logger.log_file_error()