from PySide6.QtWidgets import QMessageBox
from . import state

def prompt_box():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setWindowTitle("Question")
    msg.setText(state.msg_box_contents)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    def response(result):
        if result == QMessageBox.Yes:
            state.msg_box_response = "y"
        elif result == QMessageBox.No:
            state.msg_box_response = "n"
    msg.finished.connect(response)
    msg.exec()