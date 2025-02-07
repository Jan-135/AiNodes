from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.core.socket import Socket


class OutputSocket(Socket):
    def __init__(self, node, data_type: str):
        super().__init__(node, data_type)
        self.value = None  # Speichert den berechneten Wert der Node

    def pass_data(self):
        """Gibt einfach seinen gespeicherten Wert zurück."""

        return self.node.execute()  # Falls Wert noch nicht gesetzt, bleibt es None

    def connect(self, input_socket: "InputSocket"):
        input_socket.connect(self)
