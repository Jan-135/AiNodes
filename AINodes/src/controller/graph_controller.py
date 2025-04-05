import json

from PySide6.QtCore import QObject

from AINodes.src.core.node_editor import NodeEditor
from AINodes.src.sockets.input_socket import InputSocket
from AINodes.src.ui.node_scene import NodeScene


class GraphController(QObject):
    """
    Zentrale Controller-Klasse für das Node-Editor-System.
    - Vermittelt zwischen Model (NodeEditor) und View (GraphView).
    - Behandelt Benutzerinteraktionen (z. B. Hinzufügen/Verbinden von Nodes).
    """

    def __init__(self, node_editor: NodeEditor = None, graph_scene: NodeScene = None):
        """
        Initialisiert den GraphController.

        :param graph_scene: Die grafische Oberfläche für den Node-Graphen.
        :param node_editor: Das Model für den Node-Editor.
        """
        super().__init__()
        self.graph_scene = graph_scene
        self.node_editor = node_editor

        self.start_socket = None

    def add_node(self, node_type: str):
        """
        Erstellt einen neuen Node und fügt ihn sowohl im Model als auch in der View hinzu.

        :param node_type: Der Typ des zu erstellenden Nodes.
        :param position: Die Position, an der der Node eingefügt werden soll.
        """
        # Neues Node-Objekt im Model erstellen
        node = self.node_editor.add_new_node(node_type)
        if node:
            self.graph_scene.add_node_view(node)  # In der View anzeigen

    def delete_node(self, node_id: str) -> None:
        """
        Entfernt einen Node aus dem Model und der View.

        :param node_id: Die ID des zu entfernenden Nodes.
        """
        node = self.node_editor.get_node_by_id(node_id)
        if node:
            self.node_editor.remove_node(node)
            self.graph_scene.remove_node_view(node_id)

    def create_connection(self, output_socket_id: str, input_socket_id: str) -> None:
        """
        Erstellt eine Verbindung zwischen einem Output- und einem Input-Socket.

        :param output_socket_id: Die ID des Output-Sockets.
        :param input_socket_id: Die ID des Input-Sockets.
        """

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
            input_socket.connected_socket = None  # Verbindung im Model löschen
            self.graph_scene.remove_connection_view(output_socket_id, input_socket_id)  # View aktualisieren

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