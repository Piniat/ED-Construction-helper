from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, QObject
from helper_gui import Ui_MainWindow
from app import AppWorker
from modules import state, set_app_mode
import configparser
import glob
import os
#import pdb; pdb.set_trace()

def get_latest_journal():
    latest_file = glob.glob(os.path.join(state.journal_folder, 'Journal.*.log'))
    if not latest_file:
        print("No journal files found.")
    state.journal_file_path = max(latest_file, key=os.path.getctime)
    print(state.journal_file_path)

config = configparser.ConfigParser()
config.read('config.ini')
config.sections()
state.journal_folder = config['JOURNAL_PATH']['path']
print(config['JOURNAL_PATH']['path'])
print(state.journal_folder)
get_latest_journal()


class MainApp(QMainWindow, QObject):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.quit_button.clicked.connect(self.close)
        self.ui.pushButton_3.clicked.connect(set_app_mode.set_journal_mode)
        self.ui.pushButton.clicked.connect(set_app_mode.set_delivery_tracker)

        # Setup worker and thread
        self.worker = AppWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        # Connect signals from worker to UI updates
        self.worker.progress_updated.connect(self.ui.progressBar.setValue)
        self.worker.list_updated.connect(self.ui.textBrowser_3.setHtml)
        self.worker.percent_html_updated.connect(self.ui.Percent_display.setHtml)
        self.worker.information_panel.connect(self.ui.extra_info.setHtml)
        

        # Start the background loop when thread starts
        self.thread.started.connect(self.worker.main_loop)
        self.thread.start()

if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()