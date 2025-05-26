from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from modules import copy_lists, state, create_shopping_list_dialog

class prompt_user_creation(QDialog):
    def __init__(self, parent = None, modal = True):
        super().__init__(parent, modal=modal)
        self.setWindowTitle("Choose an action")
        self.resize(400, 100)

        layout =  QVBoxLayout(self)
        layout.addWidget(QLabel("Shopping list not found. Please choose an action"))

        create_new = QPushButton("Create list manually", self)
        cp_delivery = QPushButton("Copy data from construction list", self)
        cancel = QPushButton("Cancel", self)

        layout.addWidget(create_new)
        layout.addWidget(cp_delivery)
        layout.addWidget(cancel)

        create_new.clicked.connect(self.new_and_close)
        cp_delivery.clicked.connect(self.copy_and_close)
        cancel.clicked.connect(self.cancel_and_set)

    def new_and_close(self):
        state.app_mode = None
        self.reject()
        create_shopping_list_dialog.open_input_dialog(self)
        state.app_mode = "shopping"

    def copy_and_close(self):
        state.app_mode = None
        self.reject()
        copy_lists.copy_delivery_to_shopping(self)
        state.app_mode = "shopping"

    def cancel_and_set(self):
        state.app_mode = None
        self.reject()