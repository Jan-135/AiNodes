from AINodes.src.core.input_node import InputNode

class SingleFloatInputNode(InputNode):
    """
    A node that provides a fixed floating-point value as output.
    - This node generates a predefined float value when executed.
    """

    def __init__(self, node_id: str, value: float = 0.0):
        """
        Initializes a single-float input node with a fixed value.

        :param node_id: A unique identifier for the node.
        :param value: The predefined float value that this node will output.
        """
        super().__init__(node_id)
        self.value: float = value  # Stores the predefined float value

        # Output socket for the float value
        self.output = self.add_socket("output", "float", "out")

    def compute(self) -> float:
        """
        Returns the stored float value.

        :return: The predefined float value.
        """

        return self.value
