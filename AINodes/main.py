import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Fügt das aktuelle Verzeichnis hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))  # Fügt den src-Ordner hinzu

from src.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
