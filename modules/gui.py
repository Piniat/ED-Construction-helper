import sys
import time
from . import state, exit_app, clean_screen

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6.QtGui import QFont

def gui_run():
    class EmittingStream:
        def __init__(self, text_edit):
            self.text_edit = text_edit

        def write(self, text):
            self.text_edit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
            self.text_edit.insertPlainText(text)


        def flush(self):
            pass  # Required for compatibility
    # Subclass QMainWindow to customize your application's main window
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("ED Construction helper")
            layout = QVBoxLayout()
            layout.setSpacing(1)

            # Buttons
            exit_button = QPushButton("Exit")
            mode1 = QPushButton("Delivery tracker")
            mode2 = QPushButton("Shopping list")
            mode3 = QPushButton("Journal monitor")

            layout.addWidget(QLabel("ED Construction helper v2.0.0-alpha"))
            layout.addWidget(QLabel("Link to the latest release: https://api.github.com/repos/Piniat/ED-Construction-helper/releases/latest"))

            # Output text area
            self.output = QTextEdit()
            self.output.setReadOnly(True)
            layout.addWidget(self.output)
            font = QFont("Courier New")
            font.setStyleHint(QFont.StyleHint.Monospace)
            self.output.setFont(font)


            # Add buttons
            layout.addWidget(mode1)
            layout.addWidget(mode2)
            layout.addWidget(mode3)
            layout.addWidget(exit_button)

            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

            # Button connections
            exit_button.clicked.connect(self.exit_app_gui)
            mode1.clicked.connect(self.app_mode_1)
            mode2.clicked.connect(self.app_mode_2)
            mode3.clicked.connect(self.app_mode_3)

        
        def exit_app_gui(self):
            reply = QMessageBox.question(self, "Confirm Exit", "Are you sure you want to exit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                exit_app.close_app()
        
        def app_mode_1(self):
            state.app_mode = "1"
            state.switched = True
            sys.stdout = EmittingStream(window.output)
            sys.stderr = EmittingStream(window.output)

        def app_mode_2(self):
            state.app_mode = "2"
            state.switched = True
            sys.stdout = EmittingStream(window.output)
            sys.stderr = EmittingStream(window.output)

        def app_mode_3(self):
            state.app_mode = "3"
            state.switched = True
            sys.stdout = EmittingStream(window.output)
            sys.stderr = EmittingStream(window.output)
        
        def clear_output(self):
            # This will clear the QTextEdit output area
            clean_screen.clear_screen(self.output)

    #not sure what this does yet
    app = QApplication(sys.argv)
    window = MainWindow()
    #makes the window show
    window.show()

    # Now it's safe to redirect stdout/stderr
    sys.stdout = EmittingStream(window.output)
    sys.stderr = EmittingStream(window.output)

    #keeps the app running
    app.exec()
