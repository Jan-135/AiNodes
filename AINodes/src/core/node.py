from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, node_id):
        self.node_id = node_id
        self.output_cache = None

    def get_id(self):
        return self.node_id

    def execute(self):
        """If already executed use the output_cache"""

        if self.output_cache is not None:
            return self.output_cache

        result = self.compute()
        self.output_cache = result
        return result

    @abstractmethod
    def compute(self):
        pass

    def add_socket(self, socket_type: str, data_type: str, socket_key: str):
        pass
