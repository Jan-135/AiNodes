from AINodes.src.core.input_node import InputNode


class SingleStringInputNode(InputNode):
    def __init__(self, node_id, value=""):
        """Erzeugt eine Single-String-Input-Node mit einem festen Wert."""
        super().__init__(node_id)
        self.value = value

        # Output-Socket für den String-Wert
        self.output = self.add_socket("output", "string", "out")

    def compute(self):
        return self.value
