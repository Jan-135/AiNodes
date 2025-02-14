import json
import os

from AINodes.src.core.node import Node
from AINodes.src.core.output_node import OutputNode
from AINodes.src.scripts import generate_nodes_json

# Path to nodes.json in the data folder
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
NODES_JSON_PATH = os.path.join(DATA_DIR, "nodes.json")


class NodeEditor:
    """
    Manages nodes in the system.
    - Stores, removes, and executes nodes.
    - Handles cache resets when needed.
    """

    def __init__(self, json_file="nodes.json"):
        """
        Initializes the NodeEditor and loads the node factory.

        If the JSON file does not exist or is empty, it will automatically generate a new one.

        :param json_file: The filename of the node configuration JSON file.
        """
        if not os.path.exists(NODES_JSON_PATH) or os.stat(NODES_JSON_PATH).st_size == 0:
            print("⚠ `nodes.json` is missing or empty – Generating a new file...")
            generate_nodes_json.find_nodes()  # Automatically generate the JSON file

        self.nodes = []
        self.node_factory = self.load_node_factory(NODES_JSON_PATH)

    @staticmethod
    def load_node_factory(json_file) -> {}:
        """
        Loads the node factory dictionary from a JSON file.

        :param json_file: The path to the JSON file containing node mappings.
        :return: A dictionary mapping node names to their respective classes.
        """
        with open(json_file, "r") as f:
            node_mapping = json.load(f)

        factory = {}
        for node_name, class_path in node_mapping.items():
            module_name, class_name = class_path.rsplit(".", 1)
            module = __import__(module_name, fromlist=[class_name])
            node_class = getattr(module, class_name)
            factory[node_name] = node_class

        return factory

    def create_node(self, node_type: str) -> Node:
        """
        Creates a node based on a given string identifier.

        :param node_type: The type of node to create.
        :return: An instance of the created node.
        :raises ValueError: If the specified node type does not exist.
        """
        node_class = self.node_factory.get(node_type)
        print(self.node_factory)
        print(node_type)
        print(node_class)
        if node_class:
            return node_class(node_type)
        else:
            raise ValueError(f"Unknown node type: {node_type}")

    def add_new_node(self, node_type: str) -> Node:
        """
        Creates and adds a new node to the editor.

        :param node_type: The type of node to create.
        :return: The newly created node.
        """
        new_node = self.create_node(node_type)
        self.add_node(new_node)
        return new_node

    def add_node(self, node: "Node") -> None:
        """
        Adds an existing node to the editor.

        :param node: The node instance to be added.
        """
        self.nodes.append(node)

    def remove_node(self, node: "Node") -> None:
        """
        Removes a node from the editor.

        :param node: The node instance to be removed.
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

        Steps:
        1. Clears all caches to ensure a fresh execution.
        2. Identifies all output nodes in the system.
        3. Executes each output node to process data.
        """
        self.clear_all_caches()

        for node in self.nodes:
            if isinstance(node, OutputNode):
                node.execute()
