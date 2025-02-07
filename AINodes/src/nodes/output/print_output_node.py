from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.core.output_node import OutputNode


class PrintOutputNode(OutputNode):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.inputs.append(InputSocket(self, "string"))

    def add_input(self, socket):
        pass  # Already defined in constructor

    def execute(self):

        if self.check_if_connected():
            print(f"Output Node {self.node_id} received: {self.inputs[0].pass_data()}")
        else:
            print(f"This node is missing at least one input: {self.node_id} ")
