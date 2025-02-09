from AINodes.src.core.input_node import InputNode


class SingleFloatInputNode(InputNode):
    def __init__(self, node_id, value=0.0):
        """Erzeugt eine Single-Float-Input-Node mit einem festen Wert."""
        super().__init__(node_id)
        self.value = value

        # Output-Socket für den Wert
        self.output = self.add_socket("output", "float", "out")

    def compute(self):
        self.outputs[0].value = self.value
        return self.value
