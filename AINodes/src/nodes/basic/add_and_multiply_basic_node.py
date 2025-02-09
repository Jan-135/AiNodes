from AINodes.src.core.basic_node import BasicNode
from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.sockets.output_socket import OutputSocket


class AddAndMultiplyBasicNode(BasicNode):
    def __init__(self, node_id):
        super().__init__(node_id)

        # Zwei Input-Sockets
        self.input1 = self.add_socket("input", "float", "input_1")
        self.input2 = self.add_socket("input", "float", "input_2")

        # Zwei Output-Sockets mit benannten Keys
        self.output1 = self.add_socket("output", "float", "sum")
        self.output2 = self.add_socket("output", "float", "product")

    def compute(self):
        """Berechnet zwei Werte und speichert sie als Dictionary."""
        val1 = self.input1.pass_data()
        val2 = self.input2.pass_data()

        if val1 is None or val2 is None:
            return None

        return {
            "sum": val1 + val2,
            "product": val1 * val2
        }
