from abc import ABC, abstractmethod

from AINodes.src.core.node import Node


class OutputNode(Node, ABC):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.inputs = []

    @abstractmethod
    def add_input(self, socket):
        pass

    def execute(self):
        pass

