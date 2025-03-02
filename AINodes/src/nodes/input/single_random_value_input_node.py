import random

from AINodes.src.core.input_node import InputNode


class SingleRandomValueInputNode(InputNode):
    """
    A node that generates a random floating-point value.
    - The value is randomly selected from a specified range (min_value to max_value).
    """

    def __init__(self, node_type: str, min_value: float = 0.0, max_value: float = 1.0):
        """
        Initializes a single random value input node.

        :param node_type: A unique identifier for the node.
        :param min_value: The minimum possible generated value (inclusive).
        :param max_value: The maximum possible generated value (inclusive).
        """
        super().__init__(node_type)
        self.min_value: float = min_value
        self.max_value: float = max_value

        # Output socket for the random float value
        self.output = self.add_socket("output", "float", "random_value")

    def compute(self) -> float:
        """
        Generates and returns a random floating-point number within the defined range.

        :return: A randomly generated float between min_value and max_value.
        """
        return random.uniform(self.min_value, self.max_value)
