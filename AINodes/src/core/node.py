from abc import ABC, abstractmethod
from typing import Any, Optional


class Node(ABC):
    """
    Abstract base class for all nodes in the system.
    - Provides core functionalities such as execution, caching, and socket management.
    - Must be extended by specific node types.
    """

    def __init__(self, node_id: str):
        """
        Initializes a node with a unique identifier and an output cache.

        :param node_id: A unique identifier for the node.
        """
        self.node_id: str = node_id  # Unique identifier for the node
        self.output_cache: Optional[Any] = None  # Cache for the last computed output

    def get_id(self) -> str:
        """
        Returns the unique identifier of the node.

        :return: The node's ID as a string.
        """
        return self.node_id

    def execute(self) -> Any:
        """
        Executes the node's computation.
        - If the node has already been executed, returns the cached output.
        - Otherwise, computes the result and stores it in the cache.

        :return: The computed output or cached value.
        """
        if self.output_cache is not None:
            return self.output_cache  # Return cached result if available

        result = self.compute()  # Perform computation
        self.output_cache = result  # Store result in cache
        return result

    def reset_cache(self) -> None:
        """
        Clears the cached output so that the node will recompute its value on the next execution.
        """
        self.output_cache = None

    @abstractmethod
    def compute(self) -> Any:
        """
        Abstract method that must be implemented by subclasses.
        Defines the node's computation logic.

        :return: The computed result.
        """
        pass

    def add_socket(self, socket_type: str, data_type: str, socket_key: str) -> None:
        """
        Adds an input or output socket to the node. This method should be overridden by subclasses.

        :param socket_type: "input" or "output", defining the type of socket.
        :param data_type: The expected data type of the socket (e.g., "float", "string").
        :param socket_key: A unique identifier for the socket in its node.
        """
        pass
