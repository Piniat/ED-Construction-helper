from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, QObject
from helper_gui import Ui_MainWindow
from app import AppWorker
from modules import state, set_app_mode, create_shopping_list_dialog
from dialogs import copy_dialog, delete_list_dialog, list_creation_ask
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
        copy_list_dialog = copy_dialog.ListCopy(parent=self)
        delete_dialog_list = delete_list_dialog.DeleteList(parent=self)
        user_resolve = list_creation_ask.prompt_user_creation(parent=self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.quit_button.clicked.connect(self.close)
        self.ui.pushButton_3.clicked.connect(set_app_mode.set_journal_mode)
        self.ui.pushButton.clicked.connect(set_app_mode.set_delivery_tracker)
        self.ui.pushButton_2.clicked.connect(set_app_mode.set_shopping_list)
        self.ui.create_shopping.clicked.connect(lambda: create_shopping_list_dialog.open_input_dialog(self))
        self.ui.copy_list.clicked.connect(lambda: copy_list_dialog.exec())
        self.ui.delete_file.clicked.connect(lambda: delete_dialog_list.exec())


        # Setup worker and thread
        self.worker = AppWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        # Connect signals from worker to UI updates
        self.worker.progress_updated.connect(self.ui.progressBar.setValue)
        self.worker.list_updated.connect(self.ui.textBrowser_3.setHtml)
        self.worker.percent_html_updated.connect(self.ui.Percent_display.setHtml)
        self.worker.information_panel.connect(self.ui.extra_info.setHtml)
        self.worker.trips_display.connect(self.ui.trip_display.setHtml)
        self.worker.creation_ask.connect(lambda: user_resolve.exec())
        

        # Start the background loop when thread starts
        self.thread.started.connect(self.worker.main_loop)
        self.thread.start()

if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()
