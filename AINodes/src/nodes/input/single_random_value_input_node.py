import random
from AINodes.src.core.input_node import InputNode
from AINodes.src.sockets.output_socket import OutputSocket

class SingleRandomValueInputNode(InputNode):
    def __init__(self, node_id, min_value=0, max_value=10):
        """Erzeugt zufällige Werte zwischen min_value und max_value."""
        super().__init__(node_id)
        self.min_value = min_value
        self.max_value = max_value
        self.output = OutputSocket(self, "float", "random_value")
        self.outputs.append(self.output)

    def execute(self):
        """Gibt einen zufälligen Wert zurück."""
        return random.uniform(self.min_value, self.max_value)
