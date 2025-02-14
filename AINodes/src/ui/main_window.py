from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QToolBar, QMenu, QPushButton

from AINodes.src.ui.graph_view import GraphView
from AINodes.src.ui.node_scene import NodeScene
from AINodes.src.core.node_editor import NodeEditor


class MainWindow(QMainWindow):
    """
    Main window for the node-based AI editor.
    - Displays a toolbar with a dropdown menu for node selection.
    - Allows users to create nodes dynamically.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node-based AI Editor")
        self.setGeometry(100, 100, 800, 600)

        # Initialize Node Scene & View
        self.scene = NodeScene()
        self.view = GraphView(self.scene)
        self.setCentralWidget(self.view)

        # Initialize Node Editor
        self.node_editor = NodeEditor()

        # Create Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Create "Add Node" button (which opens a dropdown menu)
        self.add_node_button = QPushButton("Add Node", self)
        self.add_node_button.setMenu(self.create_node_menu())  # Assign the dropdown menu

        # Add Button to Toolbar
        self.toolbar.addWidget(self.add_node_button)

    def create_node_menu(self):
        """
        Creates a dropdown menu listing all available nodes.
        :return: A QMenu object with node options.
        """
        menu = QMenu(self)

        # Add each node as a selectable action
        for node_name in self.node_editor.node_factory.keys():
            action = menu.addAction(node_name)
            action.triggered.connect(lambda checked=False, name=node_name: self.add_selected_node(name))

        return menu

    def add_selected_node(self, node_type):
        """
        Adds the selected node from the dropdown menu to the scene.
        :param node_type: The type of node to create.
        """
        new_node = self.node_editor.add_new_node(node_type)  # Create new node
        self.scene.add_new_node(new_node)


    def keyPressEvent(self, event):
        """
        Closes the application when the Escape key is pressed.
        """
        if event.key() == Qt.Key_Escape:
            self.close()
