import numpy as np
from AINodes.src.core.basic_node import BasicNode
from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.sockets.output_socket import OutputSocket


class BuildArrayBasicNode(BasicNode):
    def __init__(self, node_id):
        """Erstellt ein Array basierend auf einer Zufalls-Node und einer Längen-Node."""
        super().__init__(node_id)

        # Input-Sockets: Zufallswert-Quelle & Array-Länge
        self.random_input = self.add_socket("input", "float", "random_input")
        self.length_input = self.add_socket("input", "float", "array_length")

        # Output-Socket für das generierte Array
        self.output = self.add_socket("output", "array", "generated_array")

    def compute(self):
        """Erzeugt ein Array mit neuen Zufallswerten für jede Abfrage."""
        array_length = self.length_input.pass_data()

        if array_length is None:
            print("Fehlende Eingaben für BuildArrayNode")
            return None

        # Erzeuge ein Array mit neuen Zufallswerten für jede Iteration
        generated_array = [self.random_input.pass_data() for _ in range(int(array_length))]

        return {"generated_array": generated_array}
