import json
import os
import uuid
from pprint import pprint
from typing import Dict

from AINodes.src.core.node import Node
from AINodes.src.core.output_node import OutputNode
from AINodes.src.scripts import generate_nodes_json
from AINodes.src.sockets.socket import Socket

# Path to nodes.json in the data folder
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
NODES_JSON_PATH = os.path.join(DATA_DIR, "nodes.json")

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from AINodes.src.controller.graph_controller import GraphController


class NodeEditor:
    """
    Manages nodes in the system.
    - Stores, removes, and executes nodes.
    - Handles cache resets when needed.
    """

    def __init__(self, controller, json_file="nodes.json"):
        """
        Initializes the NodeEditor and loads the node factory.

        If the JSON file does not exist or is empty, it will automatically generate a new one.

        :param json_file: The filename of the node configuration JSON file.
        """
        if not os.path.exists(NODES_JSON_PATH) or os.stat(NODES_JSON_PATH).st_size == 0:
            print("⚠ `nodes.json` is missing or empty – Generating a new file...")
            generate_nodes_json.find_nodes()  # Automatically generate the JSON file

        self.controller = controller

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

    def create_node(self, node_type: str, id=None, parameters: Dict ={}) -> Node:
        """
        Creates a node based on a given string identifier.

        :param node_type: The type of node to create.
        :return: An instance of the created node.
        :raises ValueError: If the specified node type does not exist.
        """
        node_class = self.node_factory.get(node_type)

        if node_class:
            new_node = node_class(node_type, **parameters)
            if id is None:
                new_node.set_id(str(uuid.uuid4()))
            else:
                new_node.set_id(id)

            return new_node
        else:
            raise ValueError(f"Unknown node type: {node_type}")

    def add_new_node(self, node_type: str) -> Node:
        """
        Creates and adds a new node to the editor.

        :param node_type: The type of node to create.
        :return: The newly created node.
        """
        new_node = self.create_node(node_type)
        print(new_node)
        self.nodes.append(new_node)
        return new_node

    def add_node(self, node: Node) -> None:
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

    def connect_sockets(self, start_socket: Socket, end_socket: Socket) -> None:
        start_socket.connect(end_socket)

    def connect_sockets_by_id(self, output_socket_id: str, input_socket_id: str) -> None:
        output_socket = self.get_socket_by_id(output_socket_id)
        input_socket = self.get_socket_by_id(input_socket_id)

        output_socket.connect(input_socket)

    def get_node_by_id(self, node_id: str) -> Node:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def remove_node_by_id(self, node_id: str) -> None:
        """Entfernt einen Node anhand seiner ID."""
        self.nodes = [node for node in self.nodes if node.node_id != node_id]

    def get_node_types(self) -> list:
        return list(self.node_factory.keys())

    def get_socket_by_id(self, socket_id):
        """Sucht einen Socket anhand seiner ID."""
        for node in self.nodes:
            for socket in node.inputs + node.outputs:
                if socket.socket_id == socket_id:
                    return socket
        return None

    def serialize_graph(self) -> dict:
        data = {
            "nodes": []
        }

        for node in self.nodes:
            node_data = {
                "position": self.controller.get_position(node.get_id()),
                "id": node.get_id(),
                "type": node.__class__.__name__,
                "params": node.serialize_parameters(),
                "input_connections": node.serialize_sockets(),
                "parameters": node.serialize_parameters()
            }
            data["nodes"].append(node_data)
        return data

    def save_graph_to_file(self, filepath: str):
        graph_data = self.serialize_graph()
        print(graph_data)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=4)

    def load_graph_from_file(self, filepath: str):
        node_registry = self.load_node_factory(NODES_JSON_PATH)

        with open(filepath, "r", encoding="utf-8") as f:
            graph_data = json.load(f)

        id_to_node = {}

        for node_data in graph_data["nodes"]:
            if node_data["type"] in node_registry:
                parameters = node_data.get("parameters", {})
                new_node = self.create_node(node_data["type"], id = node_data["id"], parameters =  parameters)
                x = node_data["position"]["x"]
                y = node_data["position"]["y"]

                self.controller.add_node(new_node, x, y)
                id_to_node[node_data["id"]] = new_node

        for node_data in graph_data["nodes"]:
            this_node = id_to_node.get(node_data["id"])
            input_conns = node_data.get("input_connections", {})

            for input_key, conn in input_conns.items():
                if conn is None:

                    continue

                from_node = id_to_node.get(conn["connected_node"])
                if not from_node:

                    continue


                out_socket = next((s for s in from_node.outputs if s.socket_name == conn["connected_socket"]), None)
                in_socket = next((s for s in this_node.inputs if s.socket_name == input_key), None)

                if out_socket and in_socket:
                    print("Weiter gegeben an Controller")
                    self.controller.create_connection(out_socket.socket_id, in_socket.socket_id)
