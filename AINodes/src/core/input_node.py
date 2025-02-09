from abc import ABC, abstractmethod

from AINodes.src.core.node import Node
from AINodes.src.sockets.output_socket import OutputSocket


class InputNode(Node, ABC):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.outputs = []

    def add_socket(self, socket_type: str, data_type: str, socket_key: str):
        """Creates and adds a new output socket to the node."""
        if socket_type == "output":
            socket = OutputSocket(self, data_type, socket_key)
            self.outputs.append(socket)
        elif socket_type == "input":
            raise ValueError("Can not put input socket on a input node.")
        else:
            raise ValueError("Invalid socket type. Valid types: 'input' or 'output'.")

        return socket


