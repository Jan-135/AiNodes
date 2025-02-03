from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsScene, QGraphicsLineItem

from ..core.connection import Connection
from ..core.connection_point import ConnectionPoint
from ..core.node import Node


class NodeEditor(QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.nodes = []
        self.connections = []
        self.pending_connection = None  # Speichert die erste gewählte ConnectionPoint
        self.temp_line = None  # Temporäre Verbindungslinie

    def add_node(self, x, y):
        node = Node(x, y)
        self.addItem(node)
        self.nodes.append(node)

        for connection_point in node.inputs + node.outputs:
            self.addItem(connection_point)



    def delete_selected_nodes(self):
        for item in self.selectedItems():
            if isinstance(item, Node):
                # Entferne alle Verbindungen des Nodes
                connections_to_remove = [conn for conn in self.connections
                                         if conn.start_socket in item.inputs + item.outputs
                                         or conn.end_socket in item.inputs + item.outputs]
                for conn in connections_to_remove:
                    self.removeItem(conn)
                    self.connections.remove(conn)

                connection_points_to_remove = [point for point in item.inputs + item.outputs]
                for point in connection_points_to_remove:
                    self.removeItem(point)




                # Entferne den Node selbst
                self.removeItem(item)
                self.nodes.remove(item)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if self.pending_connection and self.temp_line:
            start_pos = self.pending_connection.sceneBoundingRect().center()
            self.temp_line.setLine(start_pos.x(), start_pos.y(), event.scenePos().x(), event.scenePos().y())

        # Verbindungslinien updaten, falls Nodes bewegt wurden
        for connection in self.connections:
            connection.update_position()
        for node in self.nodes:
            for connection_point in node.inputs + node.outputs:
                connection_point.update_position()


    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.pending_connection and self.temp_line:
            item = self.itemAt(event.scenePos(), self.views()[0].transform())
            if not isinstance(item, ConnectionPoint):
                # Falls kein gültiges Ziel -> Temporäre Linie entfernen
                self.pending_connection.setBrush(QBrush(QColor(255, 255, 255)))
                self.pending_connection = None
                self.removeItem(self.temp_line)
                self.temp_line = None

        super().mouseReleaseEvent(event)
