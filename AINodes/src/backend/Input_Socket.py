from AINodes.src.backend.Node import Node
from AINodes.src.backend.Socket import Socket


class InputSocket(Socket):

    def __init__(self, node: Node, data_type):
        super().__init__(node, data_type)

    def pass_data(self):

        print("Halo")

        if self.connected_socket is None:
            return None
        else:
            return self.connected_socket.pass_data()