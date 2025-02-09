from abc import ABC, abstractmethod

from AINodes.src.core.node import Node
from AINodes.src.sockets.Input_socket import InputSocket


class OutputNode(Node, ABC):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.inputs = []

    def check_if_connected(self):
        """Prüft, ob alle Input-Sockets mit einem Output-Socket verbunden sind."""
        for socket in self.inputs:
            if socket.connected_socket is None:  # Prüft, ob eine Verbindung existiert
                return False
        return True

    def add_socket(self, socket_type: str, data_type: str, socket_key: str):
        """Creates and adds a new input socket to the node."""
        if socket_type == "input":
            socket = InputSocket(self, data_type, socket_key)
            self.inputs.append(socket)
        elif socket_type == "output":
            raise ValueError("Can not put output socket on an output node.")
        else:
            raise ValueError("Invalid socket type. Valid socket types: 'input' or 'output'.")
        return socket