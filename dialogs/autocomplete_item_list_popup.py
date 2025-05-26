from PySide6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QCompleter, QLabel
from PySide6.QtCore import Qt

class AutoCompleteInputDialog(QDialog):
    def __init__(self, autocomplete_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Shopping list creation")
        self.setModal(True)  # Make it modal (blocks parent interaction)
        self.resize(400, 100)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Input commodity name:"))

        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)

        self.completer = QCompleter(autocomplete_list, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.line_edit.setCompleter(self.completer)

        ok_btn = QPushButton("OK", self)
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)

    def get_input(self):
        return self.line_edit.text()