from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsSceneMouseEvent, QGraphicsItem, QGraphicsLineItem

from AINodes.src.ui.connection import Connection


class GraphicSocket(QGraphicsEllipseItem):
    pending_connection = None
    temp_line = None

    def __init__(self, x_pos, y_pos, parent_node,is_input=True):
        super().__init__(x_pos, y_pos, 10, 10, parent_node)  # Kleiner Punkt als Steckplatz
        self.setBrush(QBrush(QColor(255, 255, 255)))
        self.setPen(QPen(QColor(0, 0, 0)))
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

        self.parent_node = parent_node
        self.relative_x = x_pos
        self.relative_y = y_pos
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


        if GraphicSocket.pending_connection is None:
            self.start_connection(scene)
        else:
            self.complete_connection(scene)

    def start_connection(self, scene):
        """Startet eine neue Verbindung vom aktuellen ConnectionPoint."""
        GraphicSocket.pending_connection = self
        self.setBrush(QBrush(QColor(255, 100, 100)))  # Markierung (rot)

        # Temporäre Verbindungslinie erstellen
        GraphicSocket.temp_line = QGraphicsLineItem()
        GraphicSocket.temp_line.setPen(QPen(QColor(255, 100, 100), 2, Qt.DashLine))  # Gestrichelte Linie
        scene.addItem(GraphicSocket.temp_line)

    def complete_connection(self, scene):
        """Vollendet eine Verbindung zu einem anderen ConnectionPoint oder setzt die Verbindung zurück."""



        start_socket, end_socket = self.determine_connection_direction()

        scene.activeWindow().add_connection(start_socket, end_socket)


        GraphicSocket.reset_pending_connection()



    def determine_connection_direction(self):
        """Bestimmt, welches ConnectionPoint der Start und welches das Ende ist."""
        if GraphicSocket.pending_connection.is_input:
            return self, GraphicSocket.pending_connection
        return GraphicSocket.pending_connection, self

    @staticmethod
    def reset_pending_connection():
        """Setzt eine fehlgeschlagene oder abgeschlossene Verbindung zurück."""
        if GraphicSocket.pending_connection:
            GraphicSocket.pending_connection.setBrush(QBrush(QColor(255, 255, 255)))
        if GraphicSocket.temp_line:
            GraphicSocket.temp_line.scene().removeItem(GraphicSocket.temp_line)
            GraphicSocket.temp_line = None
        GraphicSocket.pending_connection = None

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
