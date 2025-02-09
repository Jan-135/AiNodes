from abc import ABC, abstractmethod

from AINodes.src.core.node import Node


class Socket(ABC):
    def __init__(self, node: Node, data_type: str, socket_key: str):
        self.node = node  # Reference to parent node
        self.data_type = data_type  # Type of data this socket handles
        self.socket_key = socket_key


    @abstractmethod

    def pass_data(self):
        pass
