from typing import List

from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QGraphicsScene

from AINodes.src.core.node import Node
from AINodes.src.ui.connection import Connection
from AINodes.src.ui.graphic_node import GraphicNode


class NodeScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(-500, -500, 1000, 1000)  # Setzt den sichtbaren Bereich
        self.setBackgroundBrush(QBrush(QColor(29, 29, 29)))

        self.nodes: List[GraphicNode] = []
        self.connections: List[Connection] = []

    def add_new_node(self, node: Node):

        newGraphicNode = GraphicNode(node)
        self.nodes.append(newGraphicNode)
        self.addItem(newGraphicNode)

    def add_new_connection(self):

        newGraphicConnection = Connection()
        self.connections.append(newGraphicConnection)
        self.addItem(newGraphicConnection)

