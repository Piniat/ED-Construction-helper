import shutil
import os
from PySide6.QtWidgets import QMessageBox
from . import state, print_delivery_progress, print_shopping_list

def copy_shopping_to_delivery(self):
    if os.path.isfile('Shopping_list.json'):
        if os.path.isfile('Construction_progress.json'):
            confirm = QMessageBox.question(None, "Overwrite confirmation", "This will overwrite the construction progress file (Construction_progress.json). Are you sure you want to do this?", QMessageBox.Yes | QMessageBox.No)
            if confirm != QMessageBox.Yes:
                QMessageBox.information(None, "Information", "Operation aborted")
                return
            shutil.copyfile('Shopping_list.json', 'Construction_progress.json')
            QMessageBox.information(None, "Success", "Shopping list contents copied to delivery list")
        else:
            shutil.copyfile('Shopping_list.json', 'Construction_progress.json')
            QMessageBox.information(None, "Success", "Shopping list contents copied to delivery list")
            #doesn't work
            #if state.app_mode == "delivery":
            #    print_delivery_progress.print_construction_progress(self)
            #    state.ready_to_update = True
    else:
        QMessageBox.critical(None, "Error", "Shopping list file not found")

def copy_delivery_to_shopping(self):
    if os.path.isfile('Construction_progress.json'):
        if os.path.isfile('Shopping_list.json'):
            confirm = QMessageBox.question(None, "Overwrite confirmation", "This will overwrite the shopping list file (Shopping_list.json). Are you sure you want to do this?", QMessageBox.Yes | QMessageBox.No)
            if confirm != QMessageBox.Yes:
                QMessageBox.information(None, "Information", "Operation aborted")
                return
            shutil.copyfile('Construction_progress.json', 'Shopping_list.json')
            QMessageBox.information(None, "Success", "Delivery list contents copied to shopping list")
        else:
            shutil.copyfile('Construction_progress.json', 'Shopping_list.json')
            QMessageBox.information(None, "Success", "Delivery list contents copied to shopping list")
            #if state.app_mode == "shopping":
            #    print_shopping_list.print_list(self)
            #    state.ready_to_update = True
    else:
        QMessageBox.critical(None, "Error", "Delivery list file not found")

def copy_on_new_shopping_list():
    if os.path.isfile('Construction_progress.json'):
        if os.path.isfile('Shopping_list.json'):
            confirm = QMessageBox.question(None, "This shouldn't occur here. This means that the file is here but for whatever reason the creation of a new list has been triggered. Copy anyways?", QMessageBox.Yes | QMessageBox.No)
            if confirm != QMessageBox.Yes:
                QMessageBox.information(None, "Information", "Operation aborted")
                return
            shutil.copyfile('Construction_progress.json', 'Shopping_list.json')
            QMessageBox.information(None, "Success", "Delivery list contents copied to shopping list")
        else:
            shutil.copyfile('Construction_progress.json', 'Shopping_list.json')
            QMessageBox.information(None, "Success", "Delivery list contents copied to shopping list")
    else:
        QMessageBox.critical(None, "Error", "Delivery list file not found. Please create one first before using the automated method<br>Aplication mode reset.")
        state.app_mode = None