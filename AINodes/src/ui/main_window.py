from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QToolBar, QMenu, QPushButton

from AINodes.src.controller.graph_controller import GraphController
from AINodes.src.ui.graph_view import GraphView
from AINodes.src.ui.node_scene import NodeScene


class MainWindow(QMainWindow):
    """
    Main window for the node-based AI editor.
    - Displays a toolbar with a dropdown menu for node selection.
    - Allows users to create nodes dynamically.
    """

    def __init__(self, controller: GraphController = None):
        super().__init__()
        self.setWindowTitle("Node-based AI Editor")
        self.setGeometry(100, 100, 800, 600)



        # Initialisiere Node Scene & View
        self.scene = NodeScene(controller)
        self.view = GraphView(self.scene)
        self.setCentralWidget(self.view)

        # Setze den Controller
        self.controller = controller

        # Erstelle Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Erstelle "Add Node" Button
        self.add_node_button = QPushButton("Add Node", self)
        self.add_node_button.setMenu(self.create_node_menu())
        self.toolbar.addWidget(self.add_node_button)

        self.run_button = QPushButton("Run")
        self.toolbar.addWidget(self.run_button)
        self.run_button.clicked.connect(self.on_run_button_clicked)
    def on_run_button_clicked(self):
        self.controller.run()

    def create_node_menu(self):
        """
        Creates a dropdown menu listing all available nodes.
        :return: A QMenu object with node options.
        """
        menu = QMenu(self)
        nodes_list = self.controller.get_available_nodes()

        for node_name in nodes_list:
            action = menu.addAction(node_name)
            action.triggered.connect(lambda checked=False, name=node_name: self.controller.add_node(name))

        return menu



    def keyPressEvent(self, event):
        """
        Beendet die Anwendung bei Escape.
        """
        if event.key() == Qt.Key_Escape:
            self.close()

    def set_controller(self, graph_controller):
        self.controller = graph_controller
        self.scene.controller = graph_controller
        print(graph_controller)
