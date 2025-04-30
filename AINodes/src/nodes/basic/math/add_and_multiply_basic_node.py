from typing import Optional, Dict, Union

from AINodes.src.core.basic_node import BasicNode


class AddAndMultiplyBasicNode(BasicNode):
    """
    A node that performs both addition and multiplication on two input values.
    - Takes two float inputs.
    - Outputs their sum and product.
    """

    def __init__(self, node_type: str):
        """
        Initializes an addition and multiplication node.

        :param node_type: A unique identifier for the node.
        """
        super().__init__(node_type)

        # Define input sockets
        self.input1 = self.add_socket("input", "float", "input_1")
        self.input2 = self.add_socket("input", "float", "input_2")

        # Define output sockets
        self.output1 = self.add_socket("output", "float", "sum")
        self.output2 = self.add_socket("output", "float", "product")

    def compute(self) -> Optional[Dict[str, Union[float, int]]]:
        """
        Computes the sum and product of the two input values.

        :return: A dictionary containing:
                 - "sum": The sum of input_1 and input_2.
                 - "product": The product of input_1 and input_2.
                 Returns None if either input is missing.
        """
        val1 = self.input1.pass_data()
        val2 = self.input2.pass_data()

        if val1 is None or val2 is None:
            return None  # Return None if any input is missing

        return {
            "sum": val1 + val2,
            "product": val1 * val2
        }

    def serialize_parameters(self) -> dict:
        return {

        }