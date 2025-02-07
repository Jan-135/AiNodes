from AINodes.src.core.basic_node import BasicNode
from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.sockets.output_socket import OutputSocket

class AddAndMultiplyBasicNode(BasicNode):
    def __init__(self, node_id):
        super().__init__(node_id)

        # Zwei Input-Sockets
        self.input1 = InputSocket(self, "float")
        self.input2 = InputSocket(self, "float")
        self.inputs.extend([self.input1, self.input2])

        # Zwei Output-Sockets mit benannten Keys
        self.output1 = OutputSocket(self, "float", "sum")  # Erstes Ergebnis
        self.output2 = OutputSocket(self, "float", "product")  # Zweites Ergebnis
        self.outputs.extend([self.output1, self.output2])

    def execute(self):
        """Berechnet zwei Werte und speichert sie als Dictionary."""
        val1 = self.input1.pass_data()
        val2 = self.input2.pass_data()

        if val1 is None or val2 is None:
            print(val1)
            print(val2)
            print("halloooooo")
            return None

        return {
            "sum": val1 + val2,         # Addition
            "product": val1 * val2      # Multiplikation
        }  # Gibt Dictionary zurück
