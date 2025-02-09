from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, node_id):
        self.node_id = node_id


    def get_id(self):
        return self.node_id

    @abstractmethod

    def execute(self):
        pass

    def add_socket(self, socket_type: str, data_type: str, socket_key: str):
        pass
