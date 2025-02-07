from abc import ABC, abstractmethod

from AINodes.src.core.node import Node


class Socket(ABC):
    def __init__(self, node: Node, data_type):
        self.node = node  # Reference to parent node
        self.data_type = data_type  # Type of data this socket handles


    @abstractmethod

    def pass_data(self):
        pass
