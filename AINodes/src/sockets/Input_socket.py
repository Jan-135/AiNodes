from AINodes.src.core.node import Node
from AINodes.src.core.socket import Socket

class InputSocket(Socket):
    def __init__(self, node: Node, data_type: str):
        super().__init__(node, data_type)
        self.connected_socket: "OutputSocket" | None = None  # Referenz zu einer OutputSocket

    def connect(self, output_socket: "OutputSocket"):
        if self.data_type != output_socket.data_type:
            raise TypeError("Cannot connect sockets with different data types!")
        if self.node == output_socket.node:
            raise TypeError("Cannot connect sockets of the same node!")

        self.connected_socket = output_socket  # Verbindung einseitig speichern

    def pass_data(self):
        """Zieht den Wert aus dem verbundenen OutputSocket."""
        if self.connected_socket:
            return self.connected_socket.pass_data()
        return None  # Falls keine Verbindung besteht, gib None zurück
