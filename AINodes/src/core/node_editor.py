from AINodes.src.core.node import Node
from AINodes.src.core.output_node import OutputNode
from typing import List


class NodeEditor:
    """
    Manages nodes in the system.
    - Stores, removes, and executes nodes.
    - Resets caches when needed.
    """

    def __init__(self):
        """Initializes the NodeEditor with an empty list of nodes."""
        self.nodes: List[Node] = []

    def add_node(self, node: "Node") -> None:
        """
        Adds a node to the editor.

        :param node: The node to be added.
        """
        self.nodes.append(node)

    def remove_node(self, node: "Node") -> None:
        """
        Removes a node from the editor.

        :param node: The node to be removed.
        """
        if node in self.nodes:
            self.nodes.remove(node)

    def clear_all_caches(self) -> None:
        """
        Clears the cache of all nodes to ensure fresh computations.
        """
        for node in self.nodes:
            node.reset_cache()

    def execute_all(self) -> None:
        """
        Executes all output nodes to process the computation graph.
        - First, it clears all caches to ensure a fresh execution.
        - Then, it starts execution from all output nodes.
        """
        self.clear_all_caches()

        for node in self.nodes:
            if isinstance(node, OutputNode):
                node.execute()
