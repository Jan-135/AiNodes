from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QBrush, QColor, QPen, QPainterPath, QTextOption
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem

from AINodes.src.core.node import Node
from AINodes.src.ui.graphic_socket import GraphicSocket


class GraphicNode(QGraphicsItem):
    def __init__(self, parent: Node = None, x=0, y=0):
        super().__init__()

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.node_type = parent.node_type
        self.node_id = parent.node_id

        self.num_inputs = len(parent.inputs)
        self.num_outputs = len(parent.outputs)

        self.width = 150
        self.title_height = 25
        self.body_height = min(1000, (self.num_inputs + self.num_outputs) * 30 + 10)
        self.total_height = self.title_height + self.body_height

        self.rect = QRectF(-self.width / 2, -self.total_height / 2, self.width, self.total_height)
        self.title_rect = QRectF(-self.width / 2, -self.total_height / 2, self.width, self.title_height)

        self.sockets = []
        self.socket_labels = []

        # Input-Sockets
        for i in range(self.num_inputs):
            socket_y = -self.total_height / 2 + self.title_height + (i * 30) + 15
            socket_id = parent.inputs[i].socket_id
            socket = GraphicSocket(socket_id, -self.width / 2 + 35, socket_y / 2, self)
            socket.setBrush(QBrush(QColor(48, 48, 48)))
            socket.setPen(QPen(QBrush(QColor(126, 126, 126)), 1))

            self.sockets.append(socket)

            label = QGraphicsTextItem(parent.inputs[i].socket_name, self)
            label.setDefaultTextColor(Qt.white)
            label.setPos(- self.width / 2 + 5, socket_y - 8)
            self.socket_labels.append(label)

        # Output-Sockets
        for i in range(self.num_outputs):
            socket_y = -self.total_height / 2 + self.title_height + (i * 30) + 15 + (self.num_inputs * 30)
            socket_id = parent.outputs[i].socket_id
            socket = GraphicSocket(socket_id, self.width / 2 - 40, socket_y / 2, self)
            socket.setBrush(QBrush(QColor(48, 48, 48)))
            socket.setPen(QPen(QBrush(QColor(126, 126, 126)), 1))

            self.sockets.append(socket)

            label = QGraphicsTextItem(parent.outputs[i].socket_name, self)
            label.adjustSize()
            label.document().setDefaultTextOption(QTextOption(Qt.AlignRight))
            label.setDefaultTextColor(Qt.white)

            label.setPos(self.width / 2 - label.boundingRect().width() - 5, socket_y - 8)
            self.socket_labels.append(label)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        # Titelbereich zeichnen (weicher abgerundet, fließender Übergang)
        title_path = QPainterPath()
        title_path.addRect(self.title_rect)
        painter.setBrush(QBrush(QColor(60, 120, 100)))  # Farbiger Titelbereich
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawPath(title_path)

        # Node-Hintergrund zeichnen (ohne Abrundung unten)
        painter.setBrush(QBrush(QColor(48, 48, 48)))  # Dunkelgrauer Hintergrund
        painter.setPen(QPen(QColor(0, 0, 0), 1))  # Schwarzer Rand
        painter.drawRect(self.rect.x(), self.rect.y() + self.title_height, self.rect.width(), self.body_height)

        # Titeltext zeichnen
        painter.setPen(QColor(255, 255, 255))  # Weiße Schrift
        painter.drawText(self.title_rect, Qt.AlignCenter, self.node_type)
