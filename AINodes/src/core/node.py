from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen, QPainterPath, QFont
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsTextItem, QGraphicsItemGroup, QGraphicsSceneMouseEvent

from AINodes.src.core.connection_point import ConnectionPoint


class Node(QGraphicsItemGroup):
    def __init__(self, x, y, name="Node"):
        super().__init__()
        self.setPos(x, y)
        self.setFlags(QGraphicsItemGroup.ItemIsMovable | QGraphicsItemGroup.ItemIsSelectable)  # Beweglich machen

        # Abmessungen
        self.rect_width, self.rect_height = 120, 150
        title_height = 25
        corner_radius = 10

        # Körper der Node
        body_path = QPainterPath()
        body_path.addRoundedRect(-self.rect_width / 2, -self.rect_height / 2 + title_height, self.rect_width,
                                 self.rect_height - title_height, corner_radius, corner_radius)
        self.body = QGraphicsPathItem(body_path)
        self.body.setBrush(QBrush(QColor(60, 60, 60)))  # Hellerer Grauton für den Körper
        self.body.setPen(QPen(QColor(30, 30, 30), 1))  # Dunklerer Rand

        # Titelbereich
        title_path = QPainterPath()
        title_path.addRoundedRect(-self.rect_width / 2, -self.rect_height / 2, self.rect_width,
                                  title_height + corner_radius,
                                  corner_radius, corner_radius)
        self.title = QGraphicsPathItem(title_path)
        self.title.setBrush(QBrush(QColor(45, 45, 45)))  # Dunklerer Grauton für den Titel
        self.title.setPen(QPen(Qt.NoPen))

        # Titeltext
        self.text = QGraphicsTextItem(name)
        font = QFont("Arial", 10)
        font.setBold(True)
        self.text.setFont(font)
        self.text.setDefaultTextColor(QColor(220, 220, 220))  # Hellgrauer Text
        self.text.setPos(-self.rect_width / 2 + 10, -self.rect_height / 2 + 5)

        # Verbindungspunkte (Sockets)

        socket_offset_x = self.rect_width / 2 + 5
        socket_offset_y = title_height + 15

        self.inputs : ConnectionPoint= []
        self.outputs : ConnectionPoint= []

        for i in range(2):
            input_socket = ConnectionPoint(self, -socket_offset_x,
                                           -self.rect_height / 2 + socket_offset_y + i * 30,
                                           True)
            output_socket = ConnectionPoint(self, socket_offset_x,
                                            -self.rect_height / 2 + socket_offset_y + i * 30,
                                            False)
            self.inputs.append(input_socket)
            self.outputs.append(output_socket)

        # Elemente zur Node hinzufügen
        self.addToGroup(self.body)
        self.addToGroup(self.title)
        self.addToGroup(self.text)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        print("Clicked on Node")
