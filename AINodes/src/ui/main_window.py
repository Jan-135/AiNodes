from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QToolBar

from AINodes.src.ui.graph_view import GraphView
from AINodes.src.ui.node_scene import NodeScene


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nodebasierter KI-Editor")
        self.setGeometry(100, 100, 800, 600)

        self.scene = NodeScene()
        self.view = GraphView(self.scene)
        self.setCentralWidget(self.view)

        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        action_new_node = QAction("New Node", self)

        self.toolbar.addAction(action_new_node)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

