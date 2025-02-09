from abc import ABC

from AINodes.src.core.node import Node
from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.sockets.output_socket import OutputSocket


class BasicNode(Node, ABC):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.outputs = []
        self.inputs = []

    def add_socket(self, socket_type: str, data_type: str, socket_key: str):
        """Creates and adds a new output or input socket to the node."""
        if socket_type == "input":
            socket = InputSocket(self, data_type, socket_key)
            self.inputs.append(socket)
        elif socket_type == "output":
            socket = OutputSocket(self, data_type, socket_key)
            self.outputs.append(socket)
        else:
            raise ValueError("Invalid socket type. Valid socket types: 'input' or 'output'.")
        return socket
