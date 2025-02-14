from abc import ABC, abstractmethod
from typing import List

from AINodes.src.core.node import Node
from AINodes.src.sockets.output_socket import OutputSocket


class InputNode(Node, ABC):
    """
    Abstract base class for all input nodes.
    - Input nodes generate data that flows into the computational graph.
    - They can only have output sockets (not input sockets).
    """

    def __init__(self, node_id: str):
        """
        Initializes an input node with a unique identifier.

        :param node_id: A unique identifier for the node.
        """
        super().__init__(node_id)


    def add_socket(self, socket_type: str, data_type: str, socket_key: str) -> OutputSocket:
        """
        Creates and adds a new output socket to the input node.
        - Input nodes **cannot** have input sockets.

        :param socket_type: Must be "output" (input sockets are not allowed).
        :param data_type: The expected data type of the socket (e.g., "float", "string").
        :param socket_key: A unique identifier for the socket.
        :return: The created output socket.
        :raises ValueError: If attempting to add an input socket to an input node.
        """
        if socket_type == "output":
            socket = OutputSocket(self, data_type, socket_key)
            self.outputs.append(socket)
            return socket
        elif socket_type == "input":
            raise ValueError("Cannot add an input socket to an InputNode.")
        else:
            raise ValueError("Invalid socket type. Valid types: 'input' or 'output'.")
