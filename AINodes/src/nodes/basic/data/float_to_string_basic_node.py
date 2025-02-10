from typing import Optional, Dict

from AINodes.src.core.basic_node import BasicNode


class FloatToStringBasicNode(BasicNode):
    """
    A node that converts a floating-point number into a formatted string.
    - Takes a float input and outputs a string representation with a specified precision.
    """

    def __init__(self, node_id: str, precision: int = 2):
        """
        Initializes a float-to-string conversion node.

        :param node_id: A unique identifier for the node.
        :param precision: The number of decimal places in the output string.
        """
        super().__init__(node_id)
        self.precision: int = precision  # Defines how many decimal places to include

        # Define input socket for the float value
        self.input_float = self.add_socket("input", "float", "input_float")

        # Define output socket for the string representation
        self.output_string = self.add_socket("output", "string", "string_output")

    def compute(self) -> Optional[Dict[str, str]]:
        """
        Converts the input float value into a formatted string.

        :return: A dictionary containing:
                 - "string_output": The formatted string representation of the input float.
                 Returns None if the input is missing.
        """
        value = self.input_float.pass_data()

        if value is None:
            return None  # Return None if no value is provided

        return {"string_output": f"{value:.{self.precision}f}"}  # Format float with specified precision
