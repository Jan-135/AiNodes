from typing import Optional, Dict, List, Union

from AINodes.src.core.basic_node import BasicNode


class BuildArrayBasicNode(BasicNode):
    """
    A node that generates an array based on a random value source and a specified length.
    - The random input node provides values.
    - The length input determines the size of the generated array.
    """

    def __init__(self, node_id: str):
        """
        Initializes an array-building node.

        :param node_id: A unique identifier for the node.
        """
        super().__init__(node_id)

        # Define input sockets: Random value source & array length
        self.random_input = self.add_socket("input", "float", "random_input")
        self.length_input = self.add_socket("input", "float", "array_length")

        # Define output socket for the generated array
        self.output = self.add_socket("output", "array", "generated_array")

    def compute(self) -> Optional[Dict[str, List[Union[float, int]]]]:
        """
        Generates an array with new random values for each request.

        :return: A dictionary containing:
                 - "generated_array": A list of random values.
                 Returns None if the array length input is missing.
        """
        array_length = self.length_input.pass_data()

        if array_length is None:
            print("Error: Missing input for BuildArrayBasicNode.")
            return None

        # Generate an array with new random values for each iteration
        generated_array = [self.random_input.pass_data() for _ in range(int(array_length))]

        return {"generated_array": generated_array}
