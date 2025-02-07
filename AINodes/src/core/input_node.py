from abc import ABC, abstractmethod

from AINodes.src.core.node import Node


class InputNode(Node, ABC):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.outputs = []

    @abstractmethod

    def execute(self):
        pass

