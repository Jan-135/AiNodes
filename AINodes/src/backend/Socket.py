from abc import ABC, abstractmethod

from AINodes.src.backend.Node import Node


class Socket(ABC):
    def __init__(self, node: Node, data_type):
        self.node = node  # Reference to parent node
        self.data_type = data_type  # Type of data this socket handles
        self.value = None  # Stores the actual value passed through the socket
        self.connected_socket = None  # Direct reference to another socket


    def connect(self, other_socket):
        if self.data_type != other_socket.data_type:
            raise TypeError("Cannot connect sockets with different data types!")
        if self == other_socket:
            raise TypeError("Cannot connect sockets of same node")

        self.connected_socket = other_socket
        other_socket.connected_socket = self

    @abstractmethod

    def pass_data(self):
        pass
