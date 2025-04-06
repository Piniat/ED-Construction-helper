import os
import time
import glob
import configparser
import json
from modules import state, journal_logging, exit_app, select_app_mode, shopping_list, clean_screen, del_tracking_again

def get_latest_journal():
    latest_file = glob.glob(os.path.join(state.journal_folder, 'Journal.*.log'))
    if not latest_file:
        print("No journal files found.")
    newest_file = max(latest_file, key=os.path.getctime)
    return newest_file

def start():
    clean_screen.clear_screen()
    print(f'ED Construction helper {state.current_version} \n Type "help" for a list of commands')
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    state.journal_folder
    state.journal_folder = config['JOURNAL_PATH']['path']
    journal_file_path = get_latest_journal()
    if journal_file_path == "None":
        print("No journal files found. Exiting...")
        time.sleep(1)
        exit_app.close_app()
    if not journal_file_path:
        print("No journal files found.")
        time.sleep(1)
        exit_app.close_app()
    select_app_mode.app_mode_selection()
    state.ship_cargo_space = 0
    #nice list down there huh?
    cargo_file = os.path.join(state.journal_folder, "Cargo.json")
    try:
        with open(cargo_file, "r") as cargo:
            cargo_data = json.load(cargo)
            current_cargo_list = cargo_data.get("Inventory", [])
            current_cargo_data = {item['Name']: item['Count'] for item in current_cargo_list}
    except json.JSONDecodeError:
        print(f"Json decode error")
    try:
        with open(journal_file_path) as f:
            f.seek(0, os.SEEK_END)
            while True:
                state.lines = f.readlines()
                if not state.lines and state.just_started == False and state.app_mode != "1":
                    time.sleep(0.1)
                    continue
                if state.app_mode == "3":
                    state.just_started = False
                    journal_logging.log_mode()
                elif state.app_mode == "2":
                    state.just_started = False
                    shopping_list.tracking_mode()
                elif state.app_mode == "1":
                    state.just_started = False
                    del_tracking_again.colonisation_tracker()
                    time.sleep(0.3)
    except json.JSONDecodeError:
        print(f"Json decode error")

