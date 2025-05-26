from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QSpinBox

class Item_count(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setModal = True
        self.setWindowTitle("Shopping list creation")
        self.resize(400, 100)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Input how many different commodities you need:"))
        self.spin_box = QSpinBox(self)
        self.spin_box.setRange(1, 9999)
        layout.addWidget(self.spin_box)
        ok_btn = QPushButton("OK", self)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)

    def get_input(self):
        return self.spin_box.value()