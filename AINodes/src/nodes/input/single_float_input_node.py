from AINodes.src.sockets.output_socket import OutputSocket
from AINodes.src.core.input_node import InputNode


class SingleFloatInputNode(InputNode):
    def __init__(self, node_id, value=0.0):
        super().__init__(node_id)
        self.value = value
        self.outputs.append(OutputSocket(self, "float", "out"))

    def execute(self):
        self.outputs[0].value = self.value
        return self.value
