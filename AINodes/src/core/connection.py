from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsSceneMouseEvent


class Connection(QGraphicsLineItem):
    def __init__(self, start_socket, end_socket=None):
        super().__init__()

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.setPen(QPen(QColor(200, 200, 200), 2))  # Helle graue Linie
        self.update_position()

    def update_position(self):
        start_pos = self.start_socket.sceneBoundingRect().center()
        if self.end_socket:
            end_pos = self.end_socket.sceneBoundingRect().center()
        else:
            end_pos = start_pos  # Temporäre Linie, die noch nicht verbunden ist
        self.setLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.MiddleButton:  # Mittlere Maustaste löscht die Verbindung
            self.delete_connection()

    def delete_connection(self):
        scene = self.scene()
        scene.removeItem(self)

    @classmethod
    def create(cls, start_socket, end_socket, scene):
        """ Erstellt eine gültige Verbindung oder gibt None zurück """
        # Sicherheitscheck: Ist die Verbindung bereits vorhanden?
        for item in scene.items():
            if isinstance(item, Connection) and (
                (item.start_socket == start_socket and item.end_socket == end_socket) or
                (item.start_socket == end_socket and item.end_socket == start_socket)
            ):
                print("Diese Verbindung existiert bereits.")
                return None  # Verbindung wird nicht erneut erstellt

        # Verbindung erstellen und zur Szene hinzufügen
        connection = cls(start_socket, end_socket)
        scene.addItem(connection)
        return connection