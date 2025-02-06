from AINodes.src.backend.Input_Socket import InputSocket
from AINodes.src.backend.output_node import OutputNode


class PrintOutputNode(OutputNode):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.inputs.append(InputSocket(self, "Float"))

    def add_input(self, socket):
        pass  # Already defined in constructor

    def execute(self):
        if self.inputs[0].connected_socket:
            self.inputs[0].value = self.inputs[0].connected_socket.value
        print(f"Output Node {self.node_id} received: {self.inputs[0].pass_data()}")
