from AINodes.src.backend.output_node import OutputNode


class NodeEditor:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        self.nodes.remove(node)

    def execute_all(self):
        for node in self.nodes:
            if isinstance(node, OutputNode):
                node.execute()