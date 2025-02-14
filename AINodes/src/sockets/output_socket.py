from __future__ import annotations  # Enables forward type declarations
from typing import TYPE_CHECKING, Any


from AINodes.src.sockets.socket import Socket

if TYPE_CHECKING:
    from AINodes.src.sockets.input_socket import InputSocket  # Only imported for type hints
    from AINodes.src.core.node import Node

class OutputSocket(Socket):
    """
    Represents an output socket in a node.
    - Output sockets provide data to input sockets of other nodes.
    """

    def __init__(self, node: Node, data_type: str, socket_key: str):
        """
        Initializes an output socket.

        :param node: The parent node to which this output socket belongs.
        :param data_type: The data type this socket handles (e.g., "float", "string").
        :param socket_key: A unique identifier for this socket within the node.
        """
        super().__init__(node, data_type, socket_key)

    def pass_data(self) -> any:
        """
        Retrieves the data associated with this output socket.
        - If the node's execution result is a dictionary, the method returns the
          value associated with this socket's key.
        - Otherwise, it returns the full execution result.

        :return: The data stored in the node's execution output.
        """
        result = self.node.execute()

        if isinstance(result, dict) and self.socket_key in result:
            return result[self.socket_key]

        return result

    def connect(self, input_socket: "InputSocket") -> None:
        """
        Establishes a connection between this output socket and an input socket.

        :param input_socket: The input socket to connect to.
        """
        input_socket.connect(self)
