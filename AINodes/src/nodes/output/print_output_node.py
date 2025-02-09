from AINodes.src.core.output_node import OutputNode


class PrintOutputNode(OutputNode):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.add_socket("input", "string", "input")

    def add_input(self, socket):
        pass  # Already defined in constructor

    def compute(self):
        """Gibt den Wert des Inputs aus, falls eine Verbindung besteht."""
        if self.check_if_connected():
            data = self.inputs[0].pass_data()
            if isinstance(data, list):
                formatted_data = ", ".join(f"{value:.2f}" for value in data)  # Rundet auf 2 Dezimalstellen
                print(f"Output Node {self.node_id} received: [{formatted_data}]")
            else:
                print(f"Output Node {self.node_id} received: {data}")
        else:
            print(f"This Node has no connected Input: {self.node_id}")