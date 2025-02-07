from AINodes.src.core.basic_node import BasicNode


class AddBasicNode(BasicNode):

    def __init__(self, node_id):
        super().__init__(node_id)
        self.add_input("float")
        self.add_input("float")
        self.add_output("float")

    def execute(self):
        value1 = self.inputs[0].pass_data() or 0
        value2 = self.inputs[1].pass_data() or 0
        return value1 + value2
