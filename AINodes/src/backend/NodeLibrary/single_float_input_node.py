from AINodes.src.backend.output_socket import OutputSocket
from AINodes.src.backend.input_node import InputNode


class SingleFloatInputNode(InputNode):
    def __init__(self, node_id, value=0.0):
        super().__init__(node_id)
        self.value = value
        self.outputs.append(OutputSocket(self, "Float"))

    def add_output(self, socket):
        pass  # Already defined in constructor

    def execute(self):
        self.outputs[0].value = self.value
        print("Der wert ist " + str(self.value))
        return self.value
