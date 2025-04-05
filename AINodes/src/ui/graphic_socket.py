from typing import List

from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsSceneMouseEvent, QGraphicsItem, QGraphicsLineItem

from AINodes.src.ui.connection import Connection



class GraphicSocket(QObject, QGraphicsEllipseItem):
    socket_right_clicked = Signal(str)  # 🎯 Signal KORREKT definieren

    def __init__(self, socket_id: str, x_pos, y_pos, parent_node, is_input=True):
        QObject.__init__(self)  # call to initialize properly
        QGraphicsEllipseItem.__init__(self, x_pos, y_pos, 10, 10, parent_node)
        self.setBrush(QBrush(QColor(255, 255, 255)))
        self.setPen(QPen(QColor(0, 0, 0)))
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

        self.socket_id = socket_id
        self.parent_node = parent_node
        self.relative_x = x_pos
        self.relative_y = y_pos
        self.is_input = is_input

        self.connections = []

        self.update_position()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.RightButton:
            self.socket_right_clicked.emit(self.socket_id)  # 🎯 Jetzt korrekt!
        elif event.button() == Qt.MiddleButton:
            self.delete_connections()



    def update_position(self):
        """Aktualisiert die Position des ConnectionPoints relativ zur Node."""
        if self.parent_node:
            self.setPos(self.parent_node.pos().x() + self.relative_x,
                        self.parent_node.pos().y() + self.relative_y)
