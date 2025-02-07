from abc import ABC, abstractmethod

from AINodes.src.core.node import Node


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

    @abstractmethod

    def execute(self):
        pass

