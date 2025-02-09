from AINodes.src.core.basic_node import BasicNode


class AddBasicNode(BasicNode):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.input1 = self.add_socket("input", "float", "input_1")
        self.input2 = self.add_socket("input", "float", "input_2")
        self.output = self.add_socket("output", "float", "sum")

    def compute(self):
        value1 = self.inputs[0].pass_data() or 0
        value2 = self.inputs[1].pass_data() or 0
        return value1 + value2
