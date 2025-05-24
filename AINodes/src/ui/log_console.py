from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QTextCursor

class LogConsole(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #1e1e1e; color: #dcdcdc; font-family: Consolas;")

    def log(self, message: str):
        self.append(message)
        self.moveCursor(QTextCursor.End)
