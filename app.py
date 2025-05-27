from PySide6.QtCore import QObject, Signal
import time
from modules import state, delivery_tracker, get_ship_cargo_capacity, update_gui, journal_logging, shopping_list, error_logger
import os
import configparser
import glob


class AppWorker(QObject):
    progress_updated = Signal(int)
    percent_html_updated = Signal(str)
    list_updated = Signal(str)
    information_panel = Signal(str)
    trips_display = Signal(str)
    creation_ask = Signal()
    creation_no_ask = Signal()

    def get_latest_journal(self):
        latest_file = glob.glob(os.path.join(state.journal_folder, 'Journal.*.log'))
        if not latest_file:
            print("No journal files found.")
        state.journal_file_path = max(latest_file, key=os.path.getctime)

    def main_loop(self):
        try:
            #get latest journal
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.sections()
            state.journal_folder = config['JOURNAL_PATH']['path']
            self.get_latest_journal()

            #other stuff
            self.str_percent = '<html><head/><body><p><span style=" font-size:16pt; font-weight:700;">Awaiting data...</span></p></body></html>'
            self.progress_updated.emit(0)
            get_ship_cargo_capacity.find_last_cargo_capacity()
            with open(state.journal_file_path, "r") as f:
                f.seek(0, os.SEEK_END)
                while True:
                    state.line = f.readline()
                    if state.app_mode == None:
                        self.list_updated.emit('<html><head/><body><p><span style=" font-size:12pt;">Please select a mode</span></p></body></html>')
                        time.sleep(1)
                    elif (not state.line) and ((state.initialized == True) or (state.switched == False)):
                        time.sleep(1)
                    elif state.app_mode == "delivery":
                        delivery_tracker.colonisation_tracker(self)
                        if state.ready_to_update == True:
                            print(self.event)
                            update_gui.update_lists(self)
                            state.ready_to_update = False
                        time.sleep(0.5)
                    elif state.app_mode == "journal":
                        journal_logging.display_event(self)
                        time.sleep(0.5)
                    elif state.app_mode == "shopping":
                        shopping_list.tracking_mode(self)
                        if state.ready_to_update == True:
                            print(self.event)
                            update_gui.update_lists(self)
                            state.ready_to_update = False
                        time.sleep(0.5)
        except:
            error_logger.log_file_error()
