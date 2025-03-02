from AINodes.src.core.basic_node import BasicNode
from typing import Optional, Union


class AddBasicNode(BasicNode):
    """
    A node that performs addition on two input values.
    - Takes two float inputs and outputs their sum.
    """

    def __init__(self, node_type: str):
        """
        Initializes an addition node.

        :param node_type: A unique identifier for the node.
        """
        super().__init__(node_type)

        # Define input sockets
        self.input1 = self.add_socket("input", "float", "input_1")
        self.input2 = self.add_socket("input", "float", "input_2")

        # Define output socket
        self.output = self.add_socket("output", "float", "sum")

    def compute(self) -> float:
        """
        Computes the sum of the two input values.

        :return: The sum of input_1 and input_2.
        """
        value1: Optional[Union[float, int]] = self.inputs[0].pass_data() or 0
        value2: Optional[Union[float, int]] = self.inputs[1].pass_data() or 0

        return float(value1) + float(value2)
