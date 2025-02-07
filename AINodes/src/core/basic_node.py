from abc import ABC, abstractmethod

from AINodes.src.core.node import Node
from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.sockets.output_socket import OutputSocket


class BasicNode(Node, ABC):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.outputs = []
        self.inputs = []

    def add_input(self, data_type):
        socket = InputSocket(self, data_type)
        self.inputs.append(socket)
        return socket

    def add_output(self, data_type):
        socket = OutputSocket(self, data_type)
        self.outputs.append(socket)
        return socket
