from typing import Optional, Dict, List

from AINodes.src.core.basic_node import BasicNode


class ArrayToStringBasicNode(BasicNode):
    """
    A node that converts an array into a formatted string.
    - Takes an array as input and outputs a string representation.
    - Uses a specified separator to join array elements.
    """

    def __init__(self, node_type: str, separator: str = ", "):
        """
        Initializes an array-to-string conversion node.

        :param node_type: A unique identifier for the node.
        :param separator: The separator used to join array elements in the output string.
        """
        super().__init__(node_type)
        self.separator: str = separator  # Stores the separator for formatting

        # Define input socket for the array
        self.input_array = self.add_socket("input", "array", "input_array")

        # Define output socket for the string representation
        self.output_string = self.add_socket("output", "string", "string_output")

    def compute(self) -> Optional[Dict[str, str]]:
        """
        Converts the input array into a string using the specified separator.

        :return: A dictionary containing:
                 - "string_output": The formatted string representation of the array.
                 Returns None if the input array is missing.
        """
        array_data: Optional[List] = self.input_array.pass_data()

        if array_data is None:
            return None  # Return None if no array data is provided

        return {"string_output": self.separator.join(map(str, array_data))}  # Convert array to string
