import os
from PySide6.QtWidgets import QMessageBox

def DeleteDelivery():
    if os.path.isfile("Construction_progress.json"):
        confirm = QMessageBox.question(None, "Deletion confirmation", "This will permanently delte the construction progress file (Construction_progress.json). Are you sure you want to do this?", QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            QMessageBox.information(None, "Information", "Operation aborted")
            return
        else:
            os.remove("Construction_progress.json")
            QMessageBox.information(None, "File deleted", "File deleted successfully")

def DeleteShopping():
        if os.path.isfile("Shopping_list.json"):
            confirm = QMessageBox.question(None, "Deletion confirmation", "This will permanently delte the shopping list file (Construction_progress.json). Are you sure you want to do this?", QMessageBox.Yes | QMessageBox.No)
            if confirm != QMessageBox.Yes:
                QMessageBox.information(None, "Information", "Operation aborted")
                return
            else:
                os.remove("Shopping_list.json")
                QMessageBox.information(None, "File deleted", "File deleted successfully")