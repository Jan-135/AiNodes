from AINodes.src.sockets.output_socket import OutputSocket
from AINodes.src.core.input_node import InputNode


class SingleStringInputNode(InputNode):
    def __init__(self, node_id, value=""):
        super().__init__(node_id)
        self.value = value
        self.outputs.append(OutputSocket(self, "string"))


    def execute(self):
        return self.value
