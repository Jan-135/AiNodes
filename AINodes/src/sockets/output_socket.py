from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.core.socket import Socket


class OutputSocket(Socket):
    def __init__(self, node, data_type: str, socket_key: str):
        super().__init__(node, data_type, socket_key)

    def pass_data(self):
        """Holt nur den für diesen Output-Socket relevanten Wert ab."""
        result = self.node.execute()  # Holt das Dictionary mit allen Outputs

        if isinstance(result, dict) and self.socket_key in result:
            return result[self.socket_key]  # Nur den relevanten Output zurückgeben

        return result  # Falls der Key nicht existiert

    def connect(self, input_socket: "InputSocket"):

        input_socket.connect(self)
