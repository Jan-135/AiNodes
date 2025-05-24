from typing import List

from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsSceneMouseEvent, QGraphicsItem, QGraphicsLineItem

from AINodes.src.ui.connection import Connection

class GraphicSocket(QObject, QGraphicsEllipseItem):
    socket_right_clicked = Signal(str)

    def __init__(self, socket_id: str, x_pos, y_pos, parent_node, is_input=True):
        QObject.__init__(self)
        # Define ellipse geometry relative to its local (0,0) origin
        radius = 5  # Half of the desired 10x10 size
        QGraphicsEllipseItem.__init__(self, -radius, -radius, 2*radius, 2*radius, parent_node)
        # Set the position of the item's center in the parent's coordinates
        self.setPos(x_pos, y_pos)

        # Keep the rest of your styling and flags
        self.setBrush(QBrush(QColor(48, 48, 48))) # Match node body perhaps? Or keep white.
        self.setPen(QPen(QColor(126, 126, 126), 1)) # Match node body perhaps?
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setAcceptHoverEvents(True)
        self.socket_id = socket_id
        self.is_input = is_input # Store is_input if needed
        self.connections = []
        # No need for relative_x, relative_y if using setPos like this

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        # Use the specific enum for clarity
        if event.button() == Qt.MouseButton.RightButton:
            self.socket_right_clicked.emit(self.socket_id)
        elif event.button() == Qt.MouseButton.MiddleButton:
            # Implement connection deletion logic if needed
            # self.delete_connections()
            pass
        else:
            # Important: Pass other events (like LeftButton for potential connection dragging)
            # to the base class if you don't handle them explicitly.
            super().mousePressEvent(event)

    # Optional: Add hover events for visual feedback
    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor(255, 200, 0), 1.5)) # Highlight pen on hover
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(QColor(126, 126, 126), 1)) # Restore original pen
        super().hoverLeaveEvent(event)

