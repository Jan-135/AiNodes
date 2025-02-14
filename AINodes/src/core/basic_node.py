from abc import ABC
from typing import List

from AINodes.src.core.node import Node
from AINodes.src.sockets.input_socket import InputSocket
from AINodes.src.sockets.output_socket import OutputSocket
from AINodes.src.sockets.socket import Socket


class BasicNode(Node, ABC):
    """
    A base class for nodes that process data.
    - Provides functionality for handling input and output sockets.
    - This class is intended to be inherited by more specific node types.
    """

    def __init__(self, node_id: str):
        """
        Initializes a basic node with input and output socket lists.

        :param node_id: A unique identifier for the node.
        """
        super().__init__(node_id)


    def add_socket(self, socket_type: str, data_type: str, socket_key: str) -> Socket:
        """
        Creates and adds a new input or output socket to the node.

        :param socket_type: The type of socket ('input' or 'output').
        :param data_type: The expected data type for this socket (e.g., "float", "string").
        :param socket_key: A unique identifier for the socket within the node.
        :return: The created socket (either InputSocket or OutputSocket).
        :raises ValueError: If the provided socket type is invalid.
        """
        if socket_type == "input":
            socket = InputSocket(self, data_type, socket_key)
            self.inputs.append(socket)
        elif socket_type == "output":
            socket = OutputSocket(self, data_type, socket_key)
            self.outputs.append(socket)
        else:
            raise ValueError("Invalid socket type. Valid socket types: 'input' or 'output'.")

        return socket
