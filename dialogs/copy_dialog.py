from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from modules import copy_lists

class ListCopy(QDialog):
    def __init__(self, parent = None, modal = True):
        super().__init__(parent, modal=modal)
        self.setWindowTitle("Choose an action")
        self.resize(400, 100)

        layout =  QVBoxLayout(self)
        layout.addWidget(QLabel("Choose what list you want to copy <br><b>(Warning if a list you are copying to exists it will get completely overwritten!)"))

        cp_shopping = QPushButton("Copy shopping list to delivery list", self)
        cp_delivery = QPushButton("Copy construction list to shopping list", self)
        cancel = QPushButton("Close", self)

        layout.addWidget(cp_shopping)
        layout.addWidget(cp_delivery)
        layout.addWidget(cancel)

        cp_shopping.clicked.connect(lambda: copy_lists.copy_shopping_to_delivery(self))
        cp_delivery.clicked.connect(lambda: copy_lists.copy_delivery_to_shopping(self))
        cancel.clicked.connect(self.reject)