from typing import Any

from AINodes.src.core.output_node import OutputNode
from AINodes.src.sockets.input_socket import InputSocket


class PrintOutputNode(OutputNode):
    """
    A node that prints the received input data to the console.
    - Accepts a single input socket of type "string".
    """

    def __init__(self, node_id: str):
        """
        Initializes a print output node.

        :param node_id: A unique identifier for the node.
        """
        super().__init__(node_id)
        self.add_socket("input", "string", "input")  # Adds a single input socket for strings

    def add_input(self, socket: InputSocket) -> None:
        """
        Placeholder method to prevent additional inputs from being added.
        This is because the input socket is already defined in the constructor.

        :param socket: The input socket (not used).
        """
        pass  # Already defined in constructor

    def compute(self) -> None:
        """
        Retrieves and prints the input data.
        - If the input socket is connected, fetches and prints the data.
        - If the data is a list, formats it with two decimal places.
        - If no input is connected, prints an error message.
        """
        if self.check_if_connected():
            data: Any = self.inputs[0].pass_data()
            if isinstance(data, list):
                formatted_data = ", ".join(f"{value:.2f}" for value in data)  # Rounds to 2 decimal places
                print(f"Output Node {self.node_id} received: [{formatted_data}]")
            else:
                print(f"Output Node {self.node_id} received: {data}")
        else:
            print(f"This Node has no connected Input: {self.node_id}")
