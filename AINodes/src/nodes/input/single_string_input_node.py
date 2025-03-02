from AINodes.src.core.input_node import InputNode


class SingleStringInputNode(InputNode):
    """
    A node that provides a fixed string value as output.
    - This node generates a predefined string when executed.
    """

    def __init__(self, node_type: str, value: str = ""):
        """
        Initializes a single-string input node with a fixed value.

        :param node_type: A unique identifier for the node.
        :param value: The predefined string value that this node will output.
        """
        super().__init__(node_type)
        self.value: str = value  # Stores the predefined string value

        # Output socket for the string value
        self.output = self.add_socket("output", "string", "out")

    def compute(self) -> str:
        """
        Returns the stored string value.

        :return: The predefined string value.
        """
        return self.value
