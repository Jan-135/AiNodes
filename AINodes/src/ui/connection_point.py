from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsSceneMouseEvent, QGraphicsItem, QGraphicsLineItem

from AINodes.src.ui.connection import Connection


class ConnectionPoint(QGraphicsEllipseItem):
    pending_connection = None
    temp_line = None

    def __init__(self, parent_node, x, y, is_input=True):
        super().__init__(-5, -5, 10, 10)  # Kleiner Punkt als Steckplatz
        self.setBrush(QBrush(QColor(255, 255, 255)))
        self.setPen(QPen(QColor(0, 0, 0)))
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

        self.parent_node = parent_node
        self.relative_x = x
        self.relative_y = y
        self.is_input = is_input

        # Setze Position relativ zur Node
        self.update_position()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.RightButton:  # Rechte Maustaste
            self.handle_right_click()
        elif event.button() == Qt.MiddleButton:  # Mittlere Maustaste löscht die Verbindung
            self.delete_connections()

    def handle_right_click(self):
        """Verarbeitet das Erstellen einer Verbindung durch einen Rechtsklick."""
        scene = self.scene()

        if ConnectionPoint.pending_connection is None:
            self.start_connection(scene)
        else:
            self.complete_connection(scene)

    def start_connection(self, scene):
        """Startet eine neue Verbindung vom aktuellen ConnectionPoint."""
        ConnectionPoint.pending_connection = self
        self.setBrush(QBrush(QColor(255, 100, 100)))  # Markierung (rot)

        # Temporäre Verbindungslinie erstellen
        ConnectionPoint.temp_line = QGraphicsLineItem()
        ConnectionPoint.temp_line.setPen(QPen(QColor(255, 100, 100), 2, Qt.DashLine))  # Gestrichelte Linie
        scene.addItem(ConnectionPoint.temp_line)

    def complete_connection(self, scene):
        """Vollendet eine Verbindung zu einem anderen ConnectionPoint oder setzt die Verbindung zurück."""
        if self == ConnectionPoint.pending_connection:
            return  # Verhindert Verbindung mit sich selbst

        if self.is_invalid_connection():
            print("Verbindung geht nur mit Output zu Input")
            ConnectionPoint.reset_connection()
            return

        start_socket, end_socket = self.determine_connection_direction()
        connection = Connection.create(start_socket, end_socket, scene)

        if connection:
            scene.connections.append(connection)

        ConnectionPoint.reset_connection()

    def is_invalid_connection(self):
        """Prüft, ob eine Verbindung ungültig ist (zwei Inputs oder zwei Outputs)."""
        return (self.is_input and ConnectionPoint.pending_connection.is_input) or (
                not self.is_input and not ConnectionPoint.pending_connection.is_input)

    def determine_connection_direction(self):
        """Bestimmt, welches ConnectionPoint der Start und welches das Ende ist."""
        if ConnectionPoint.pending_connection.is_input:
            return self, ConnectionPoint.pending_connection
        return ConnectionPoint.pending_connection, self

    @staticmethod
    def reset_connection():
        """Setzt eine fehlgeschlagene oder abgeschlossene Verbindung zurück."""
        if ConnectionPoint.pending_connection:
            ConnectionPoint.pending_connection.setBrush(QBrush(QColor(255, 255, 255)))
        if ConnectionPoint.temp_line:
            ConnectionPoint.temp_line.scene().removeItem(ConnectionPoint.temp_line)
            ConnectionPoint.temp_line = None
        ConnectionPoint.pending_connection = None

    def delete_connections(self):
        """Löscht alle Verbindungen, die mit diesem ConnectionPoint verbunden sind."""
        scene = self.scene()
        connections_to_remove = [conn for conn in scene.items() if isinstance(conn, Connection) and
                                 (conn.start_socket == self or conn.end_socket == self)]

        for conn in connections_to_remove:
            conn.delete_connection()

    def update_position(self):
        """Aktualisiert die Position des ConnectionPoints relativ zur Node."""
        if self.parent_node:
            self.setPos(self.parent_node.pos().x() + self.relative_x,
                        self.parent_node.pos().y() + self.relative_y)
