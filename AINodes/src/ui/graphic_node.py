from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QBrush, QColor, QPen, QPainterPath, QTextOption
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem


class GraphicNode(QGraphicsItem):
    def __init__(self, name="Node", x=0, y=0, num_inputs=1, num_outputs=1, parent=None):
        super().__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.width = 150
        self.title_height = 25
        self.body_height = min(1000, (num_inputs + num_outputs) * 30 + 10)
        self.total_height = self.title_height + self.body_height

        self.rect = QRectF(-self.width / 2, -self.total_height / 2, self.width, self.total_height)
        self.title_rect = QRectF(-self.width / 2, -self.total_height / 2, self.width, self.title_height)
        self.name = name
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        self.sockets = []
        self.socket_labels = []

        # Input-Sockets
        for i in range(num_inputs):
            socket_y = -self.total_height / 2 + self.title_height + (i * 30) + 15
            socket = QGraphicsEllipseItem(-self.width / 2 - 5, socket_y, 10, 10, self)
            socket.setBrush(QBrush(QColor(48,48,48)))  # Rot für Inputs
            socket.setPen(QPen(QBrush(QColor(126, 126, 126)), 1 ))

            self.sockets.append(socket)

            label = QGraphicsTextItem(f"Input {i + 1}", self)
            label.setDefaultTextColor(Qt.white)
            label.setPos(- self.width / 2 + 5, socket_y - 8)
            self.socket_labels.append(label)

        # Output-Sockets
        for i in range(num_outputs):
            socket_y = -self.total_height / 2 + self.title_height + (i * 30) + 15 + (num_inputs * 30)
            socket = QGraphicsEllipseItem(self.width / 2 - 5, socket_y, 10, 10, self)
            socket.setBrush(QBrush(QColor(48,48,48)))  # Grün für Outputs
            socket.setPen(QPen(QBrush(QColor(126, 126, 126)), 1))

            self.sockets.append(socket)

            label = QGraphicsTextItem(f"Output {i + 1}", self)
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
        painter.setBrush(QBrush(QColor(48,48,48)))  # Dunkelgrauer Hintergrund
        painter.setPen(QPen(QColor(0, 0, 0), 1))  # Schwarzer Rand
        painter.drawRect(self.rect.x(), self.rect.y() + self.title_height, self.rect.width(), self.body_height)

        # Titeltext zeichnen
        painter.setPen(QColor(255, 255, 255))  # Weiße Schrift
        painter.drawText(self.title_rect, Qt.AlignCenter, self.name)