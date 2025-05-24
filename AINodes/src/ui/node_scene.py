from __future__ import annotations

from typing import List
from typing import TYPE_CHECKING

from PySide6.QtGui import QColor, QBrush, QPainter
from PySide6.QtWidgets import QGraphicsScene

from AINodes.src.core.node import Node
from AINodes.src.ui.connection import Connection
from AINodes.src.ui.graphic_node import GraphicNode
from AINodes.src.ui.graphic_socket import GraphicSocket

if TYPE_CHECKING:
    from AINodes.src.controller.graph_controller import GraphController


class NodeScene(QGraphicsScene):
    def __init__(self, controller: GraphController = None, parent=None):
        super().__init__(parent)
        large_dim = 100000
        self.setSceneRect(-large_dim / 2, -large_dim / 2, large_dim, large_dim)
        self.setBackgroundBrush(QBrush(QColor(29, 29, 29)))
        self.controller = controller
        self.nodes: List[GraphicNode] = []
        self.connections: List[Connection] = []

    def register_socket(self, socket: GraphicSocket) -> None:
        socket.socket_right_clicked.connect(self.handle_socket_right_clicked)

    def add_node_view(self, node: Node, x: float = 0, y: float = 0) -> None:
        newGraphicNode = GraphicNode(node, x=x, y=y)
        self.nodes.append(newGraphicNode)
        self.addItem(newGraphicNode)
        for socket in newGraphicNode.sockets:
            self.register_socket(socket)

    def remove_node_view(self, node_id: str):
        """Entfernt eine Node anhand seiner ID."""
        for item in self.nodes:
            if isinstance(item, GraphicNode) and item.node_id == node_id:
                for socket in item.sockets:
                    for conn in getattr(socket, 'connections', []):
                        conn.delete_connection()
                self.removeItem(item)

    def add_connection_view(self, output_socket_id: str, input_socket_id: str) -> None:
        output_socket = self.find_socket_by_id(output_socket_id)
        input_socket = self.find_socket_by_id(input_socket_id)

        new_connection = Connection(output_socket, input_socket)
        self.connections.append(new_connection)
        self.addItem(new_connection)

    def find_socket_by_id(self, socket_id: str) -> GraphicSocket:
        for graphic_node in self.nodes:
            for socket in graphic_node.sockets:
                if socket.socket_id == socket_id:
                    return socket
        return None

    def handle_socket_right_clicked(self, socket_id: str):
        self.controller.connect_socket(socket_id)
