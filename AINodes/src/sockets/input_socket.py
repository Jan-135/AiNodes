from __future__ import annotations  # Enables forward type declarations
from typing import TYPE_CHECKING, Optional, Any


from AINodes.src.sockets.socket import Socket

if TYPE_CHECKING:
    from AINodes.src.sockets.output_socket import OutputSocket  # Only imported for type hints
    from AINodes.src.core.node import Node


class InputSocket(Socket):
    """
    Represents an input socket in a node.
    - Input sockets receive data from output sockets of other nodes.
    """

    def __init__(self, parent_node: Node, data_type: str, socket_name: str):
        """
        Initializes an input socket.

        :param parent_node: The parent node to which this input socket belongs.
        :param data_type: The data type this socket handles (e.g., "float", "string").
        :param socket_name: A unique identifier for this socket within the node.
        """
        super().__init__(parent_node, data_type, socket_name)
        self.connected_socket: Optional[OutputSocket] = None  # Stores reference to connected output socket

    def connect(self, output_socket: "OutputSocket") -> None:
        """
        Establishes a connection between this input socket and an output socket.
        - Ensures that both sockets have the same data type.
        - Prevents connections within the same node.

        :param output_socket: The output socket to connect to.
        :raises TypeError: If the sockets have different data types or belong to the same node.
        """
        if self.data_type != output_socket.data_type:
            raise TypeError("Cannot connect sockets with different data types!")
        if self.parent_node == output_socket.parent_node:
            raise TypeError("Cannot connect sockets of the same node!")

        self.connected_socket = output_socket  # Store the connection reference

    def pass_data(self) -> Optional[Any]:
        """
        Requests data from the connected output socket.
        - If connected, retrieves the value from the output socket.
        - If the value has changed, resets the node's cache.

        :return: The received data or None if no connection exists.
        """
        if self.connected_socket:
            new_value = self.connected_socket.pass_data()

            # Reset cache if the value has changed
            if new_value != self.parent_node.output_cache:
                self.parent_node.output_cache = None

            return new_value
        return None
