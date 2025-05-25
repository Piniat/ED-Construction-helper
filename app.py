from PySide6.QtCore import QObject, Signal
import time
from modules import state, delivery_tracker, get_ship_cargo_capacity, update_gui, journal_logging
import os


class AppWorker(QObject):
    progress_updated = Signal(int)
    percent_html_updated = Signal(str)
    list_updated = Signal(str)
    information_panel = Signal(str)

    def main_loop(self):
        self.str_percent = '<html><head/><body><p><span style=" font-size:16pt; font-weight:700;">Awaiting data...</span></p></body></html>'
        self.progress_updated.emit(0)
        print(state.journal_file_path)
        get_ship_cargo_capacity.find_last_cargo_capacity()
        with open(state.journal_file_path, "r") as f:
            f.seek(0, os.SEEK_END)
            while True:
                state.line = f.readline()
                if (not state.line) and ((state.initialized == True) or (state.switched == False)):
                    time.sleep(1)
                elif state.app_mode == None:
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
