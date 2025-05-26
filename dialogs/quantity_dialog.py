from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QSpinBox

class Quantity(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setModal = True
        self.setWindowTitle("Shopping list creation")
        self.resize(400, 100)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"How much do you need?"))
        self.quantity_spin_box = QSpinBox(self)
        self.quantity_spin_box.setRange(1, 999999)
        layout.addWidget(self.quantity_spin_box)
        ok_btn = QPushButton("OK", self)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)

    def get_input(self):
        return self.quantity_spin_box.value()