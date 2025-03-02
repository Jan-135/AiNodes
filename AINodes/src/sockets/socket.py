from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

import uuid

if TYPE_CHECKING:
    from AINodes.src.core.node import Node


class Socket(ABC):
    """
    Abstract base class for all sockets in the node system.
    - Sockets handle data flow between nodes.
    - Each socket is linked to a parent node.
    """

    def __init__(self, parent_node, data_type: str, socket_name: str):
        """
        Initializes a socket with a reference to its parent node.

        :param parent_node: The parent node to which this socket belongs.
        :param data_type: The data type this socket handles (e.g., "float", "string").
        :param socket_name: A unique identifier for this socket within the node.
        """

        self.socket_id = str(uuid.uuid4())
        self.parent_node: Node = parent_node  # Reference to parent node
        self.data_type: str = data_type  # Type of data this socket handles
        self.socket_name: str = socket_name  # Unique identifier for the socket

    @abstractmethod
    def pass_data(self):
        """
        Abstract method to be implemented by subclasses.
        Defines how data is passed through the socket.

        :return: The data being transferred through this socket.
        """
        pass

    def connect(self):
        pass
