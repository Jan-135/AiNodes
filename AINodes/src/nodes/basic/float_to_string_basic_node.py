from AINodes.src.core.basic_node import BasicNode


class FloatToStringBasicNode(BasicNode):
    def __init__(self, node_id, precision=2):
        """Wandelt einen Float-Wert in einen String um."""
        super().__init__(node_id)
        self.precision = precision

        # Input-Socket für den Float-Wert
        self.input_float = self.add_socket("input", "float", "input_float")

        # Output-Socket für den String-Wert
        self.output_string = self.add_socket("output", "string", "string_output")

    def execute(self):
        """Konvertiert den Float-Wert in einen String."""
        value = self.input_float.pass_data()

        if value is None:
            return None

        return {"string_output": f"{value:.{self.precision}f}"}