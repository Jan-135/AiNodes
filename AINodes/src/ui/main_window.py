import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Fügt das aktuelle Verzeichnis hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))  # Fügt den src-Ordner hinzu

from PySide6.QtWidgets import QMainWindow, QGraphicsView, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt
from ..ui.node_view import NodeEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Editor Prototype")
        self.setGeometry(500, 500, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.view = QGraphicsView()
        self.scene = NodeEditor()
        self.view.setScene(self.scene)
        
        self.add_node_button = QPushButton("Add Node")
        self.add_node_button.clicked.connect(self.add_node)
        
        self.layout.addWidget(self.add_node_button)
        self.layout.addWidget(self.view)
        
        self.view.setFocusPolicy(Qt.StrongFocus)

    def add_node(self):
        self.scene.add_node(0, 0)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Delete:
            self.scene.delete_selected_nodes()
        elif event.key() == Qt.Key_Escape:
            self.close()
