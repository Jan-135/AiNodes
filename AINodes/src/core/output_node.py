from abc import ABC, abstractmethod
from typing import List

from AINodes.src.core.node import Node
from AINodes.src.sockets.input_socket import InputSocket


class OutputNode(Node, ABC):
    """
    Abstract base class for all output nodes.
    - Output nodes collect data from the computation graph.
    - They can only have input sockets (not output sockets).
    """

    def __init__(self, node_id: str):
        """
        Initializes an output node with a unique identifier.

        :param node_id: A unique identifier for the node.
        """
        super().__init__(node_id)
        self.inputs: List[InputSocket] = []  # List of input sockets

    def check_if_connected(self) -> bool:
        """
        Checks whether all input sockets are connected to an output socket.

        :return: True if all input sockets are connected, False otherwise.
        """
        for socket in self.inputs:
            if socket.connected_socket is None:  # Checks if a connection exists
                return False
        return True

    def add_socket(self, socket_type: str, data_type: str, socket_key: str) -> InputSocket:
        """
        Creates and adds a new input socket to the output node.
        - Output nodes **cannot** have output sockets.

        :param socket_type: Must be "input" (output sockets are not allowed).
        :param data_type: The expected data type of the socket (e.g., "float", "string").
        :param socket_key: A unique identifier for the socket.
        :return: The created input socket.
        :raises ValueError: If attempting to add an output socket to an output node.
        """
        if socket_type == "input":
            socket = InputSocket(self, data_type, socket_key)
            self.inputs.append(socket)
        elif socket_type == "output":
            raise ValueError("Cannot add an output socket to an OutputNode.")
        else:
            raise ValueError("Invalid socket type. Valid types: 'input' or 'output'.")

        return socket
