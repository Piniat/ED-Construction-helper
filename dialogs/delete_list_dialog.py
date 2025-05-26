import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from modules import delete_lists

class DeleteList(QDialog):
    def __init__(self, parent = None, modal = True):
        super().__init__(parent, modal=modal)
        self.setWindowTitle("Choose an action")
        self.resize(400, 100)

        layout =  QVBoxLayout(self)
        layout.addWidget(QLabel("Choose what list you want to delete"))

        del_shopping = QPushButton("Delete shopping list", self)
        del_delivery = QPushButton("Delete construction list", self)
        cancel = QPushButton("Close", self)

        layout.addWidget(del_shopping)
        layout.addWidget(del_delivery)
        layout.addWidget(cancel)

        del_shopping.clicked.connect(lambda: delete_lists.DeleteShopping())
        del_delivery.clicked.connect(lambda: delete_lists.DeleteDelivery())
        cancel.clicked.connect(self.reject)