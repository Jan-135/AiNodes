import json
from typing import Dict

from PySide6.QtCore import QObject

from AINodes.src.core.node import Node
from AINodes.src.core.node_editor import NodeEditor
from AINodes.src.sockets.input_socket import InputSocket
from AINodes.src.ui.main_window import MainWindow
from AINodes.src.ui.node_scene import NodeScene
from AINodes.src.utils.logger import logger


class GraphController(QObject):
    """
    Zentrale Controller-Klasse für das Node-Editor-System.
    - Vermittelt zwischen Model (NodeEditor) und View (GraphView).
    - Behandelt Benutzerinteraktionen (z. B. Hinzufügen/Verbinden von Nodes).
    """

    def __init__(self):
        """
        Initialisiert den GraphController.

        :param graph_scene: Die grafische Oberfläche für den Node-Graphen.
        :param node_editor: Das Model für den Node-Editor.
        """
        self.node_editor = NodeEditor(self)
        self.main_window = MainWindow(self)

        handler = UILogHandler(self)
        handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
        logger.addHandler(handler)

        self.graph_scene = self.main_window.scene

        self.start_socket = None

    def forward_log_to_ui(self, message: str) -> None:
        self.main_window.log(message)

    def create_node(self, node_type: str, x: float = None, y: float = None) -> None:
        """
        Erstellt einen neuen Node und fügt ihn sowohl im Model als auch in der View hinzu.

        :param node_type: Der Typ des zu erstellenden Nodes.
        :param position: Die Position, an der der Node eingefügt werden soll.
        """
        node = self.node_editor.add_new_node(node_type)
        if node:
            if x is None or y is None:
                self.graph_scene.add_node_view(node)
            else:
                self.graph_scene.add_node_view(node, x, y)

    def delete_node_by_id(self, node_id: str) -> None:
        """
        Entfernt einen Node aus dem Model und der View.

        :param node_id: Die ID des zu entfernenden Nodes.
        """

        node = self.node_editor.get_node_by_id(node_id)
        if node:
            print("Trying to delete node by id:", node_id)
            self.node_editor.remove_node(node)
            self.graph_scene.remove_node_view(node_id)

    def create_connection(self, output_socket_id: str, input_socket_id: str) -> None:
        """
        Erstellt eine Verbindung zwischen einem Output- und einem Input-Socket.

        :param output_socket_id: Die ID des Output-Sockets.
        :param input_socket_id: Die ID des Input-Sockets.
        """
        print("Lets try in controller")

        try:
            self.node_editor.connect_sockets_by_id(output_socket_id, input_socket_id)
            print(f"Connnection worked!")
        except:
            print(f"Connection failed: {output_socket_id}, {input_socket_id}")
            return
        self.graph_scene.add_connection_view(output_socket_id, input_socket_id)
        self.start_socket = None

    def delete_connection(self, output_socket_id: str, input_socket_id: str) -> None:
        """
        Entfernt eine Verbindung zwischen einem Output- und einem Input-Socket.

        :param output_socket_id: Die ID des Output-Sockets.
        :param input_socket_id: Die ID des Input-Sockets.
        """
        input_socket = self.node_editor.get_socket_by_id(input_socket_id)

        if isinstance(input_socket, InputSocket) and input_socket.connected_socket:
            input_socket.connected_socket = None
            self.graph_scene.remove_connection_view(output_socket_id, input_socket_id)

    def get_available_nodes(self):

        nodes_list_path = "AINodes/src/data/nodes.json"
        with open(nodes_list_path, "r", encoding="utf-8") as file:
            nodes_list = json.load(file)

        return nodes_list

    def set_graph_view(self, scene):
        self.graph_scene = scene

    def connect_socket(self, socket_id: str) -> None:
        if self.start_socket is None:
            self.start_socket = socket_id
        else:
            self.create_connection(self.start_socket, socket_id)

    def run(self):
        self.node_editor.execute_all()

    def get_graph_position(self, id: str) -> (float, float):
        nodes = self.graph_scene.nodes
        for node in nodes:
            if node.node_id == id:
                position = node.pos()
                return position.x(), position.y()

    def save(self, filepath: str):
        self.node_editor.save_graph_to_file(filepath)

    def get_position(self, node_id):
        for node in self.graph_scene.nodes:
            print(f"Node id: {node.node_id}, position: {node.pos()}")
            print(f"Searching for: {node_id}")
            if node.node_id == node_id:
                return {"x": node.pos().x(), "y": node.pos().y()}

        raise Exception(f"Node {node_id} not found.")

    def load_graph(self, filepath: str):
        self.node_editor.load_graph_from_file(filepath)

    def add_node(self, node: Node, x: float = 0, y: float = 0) -> None:
        self.node_editor.nodes.append(node)
        if node:
            self.graph_scene.add_node_view(node, x, y)


import logging


class UILogHandler(logging.Handler):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def emit(self, record):
        msg = self.format(record)
        self.controller.forward_log_to_ui(msg)
