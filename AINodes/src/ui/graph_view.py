# file: AINodes/src/ui/graph_view.py
from PySide6.QtCore import Qt, QPointF, QEvent # Added QEvent
from PySide6.QtGui import QPainter, QKeyEvent # QKeyEvent might not be strictly needed now for event()
from PySide6.QtWidgets import QGraphicsView, QApplication

from AINodes.src.ui.node_search_popup import NodeSearchPopup

class GraphView(QGraphicsView):
    def __init__(self, scene, parent=None): # scene is actually NodeScene instance
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        self.search_popup = NodeSearchPopup(scene.controller, self)
        scene.addItem(self.search_popup)

        self.is_panning = False
        self.last_mouse_pos = None

        self.search_popup.node_selected.connect(self.handle_node_creation_request)

        # Ensure the view can receive keyboard focus
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


    def handle_node_creation_request(self, node_name: str, scene_pos: QPointF):
        self.scene().controller.create_node(node_name, scene_pos.x(), scene_pos.y())

    def wheelEvent(self, event):
        scale_factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        self.scale(scale_factor, scale_factor)

    def mousePressEvent(self, event):
        # Important: Ensure the view gets focus when clicked, so it can receive key events
        # This is especially important if other widgets (like the popup) were focused before.
        self.setFocus()

        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            if self.search_popup.isVisible():
                popup_rect_in_view = self.mapFromScene(self.search_popup.geometry()).boundingRect()
                if not popup_rect_in_view.contains(event.pos()):
                    self.search_popup.hide_popup()
            super().mousePressEvent(event) # Call super for other mouse buttons

    def mouseMoveEvent(self, event):
        if self.is_panning and (event.buttons() & Qt.MouseButton.MiddleButton):
            delta_view = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta_view.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta_view.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def event(self, event: QEvent) -> bool:
        """
        Override event() to intercept Tab key press before default focus handling.
        """
        if event.type() == QEvent.Type.KeyPress:
            # Cast to QKeyEvent to access key()
            key_event = QKeyEvent(event)
            if key_event.key() == Qt.Key.Key_Tab:
                # Show the search popup
                # Use current mouse position or center of view if mouse is not over view
                try:
                    # Get global cursor position
                    global_cursor_pos = self.cursor().pos()
                    # Map global position to view coordinates
                    view_mouse_pos = self.mapFromGlobal(global_cursor_pos)

                    # Check if the mapped position is within the viewport bounds
                    if not self.viewport().rect().contains(view_mouse_pos):
                        # If mouse is outside, use center of the viewport
                        view_mouse_pos = self.viewport().rect().center()
                except Exception: # Fallback if cursor().pos() gives issues
                    view_mouse_pos = self.viewport().rect().center()

                scene_mouse_pos = self.mapToScene(view_mouse_pos)
                self.search_popup.show_at(scene_mouse_pos)
                return True  # Event handled, prevent further processing (like focus change)
            elif key_event.key() == Qt.Key.Key_Escape:
                # Allow escape to also close the popup if it's visible
                if self.search_popup.isVisible():
                    self.search_popup.hide_popup()
                    return True # Event handled

        # For all other events, call the base class implementation
        return super().event(event)


    def leaveEvent(self, event):
        if self.is_panning:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)