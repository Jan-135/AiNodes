from AINodes.src.backend.socket import Socket


class OutputSocket(Socket):

    def __init__(self, node, data_type):
        super().__init__(node, data_type)

    def pass_data(self):
        print("hallo")
        return self.node.execute()