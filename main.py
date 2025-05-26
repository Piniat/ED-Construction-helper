from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread, QObject
from helper_gui import Ui_MainWindow
from app import AppWorker
from modules import set_app_mode, create_shopping_list_dialog, error_logger
from dialogs import copy_dialog, delete_list_dialog, list_creation_ask
import start_app
#import pdb; pdb.set_trace()

class MainApp(QMainWindow, QObject):
    def __init__(self):
        try:
            #gui start
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

            start_app.begin_checks(self)

            # Start the background loop when thread starts
            self.thread.started.connect(self.worker.main_loop)
            self.thread.start()
        except:
            error_logger.log_file_error()
try:
    if __name__ == "__main__":
        app = QApplication([])
        window = MainApp()
        window.show()
        app.exec()
except:
    error_logger.log_file_error()
