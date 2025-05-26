from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QTimer
from . import state

def message_box():
    msg = QMessageBox()
    msg.setWindowTitle("Information")
    msg.setText(state.msg_box_contents)
    msg.setStandardButtons(QMessageBox.NoButton)
    QTimer.singleShot(state.msg_box_close_time, msg.reject)
    msg.exec()

def message_box_close_done():
    global msg
    msg = QMessageBox()
    msg.setWindowTitle("Information")
    msg.setText(state.msg_box_contents)
    msg.setStandardButtons(QMessageBox.NoButton)
    msg.show()
    QTimer.singleShot(1000, close_box)

def close_box():
    global msg
    if msg:
        msg.close()
        msg = None