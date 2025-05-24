from PySide6.QtCore import Qt, QPointF, QEvent
from PySide6.QtGui import QPainter, QKeyEvent
from PySide6.QtWidgets import QGraphicsView, QApplication

from AINodes.src.ui.node_search_popup import NodeSearchPopup


class GraphView(QGraphicsView):
    def __init__(self, scene, parent=None):

        self.search_popup = None

        super().__init__(scene, parent)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.search_popup = NodeSearchPopup(scene.controller, self)
        if self.search_popup:
            self.search_popup.setVisible(False)
            self.search_popup.node_selected.connect(self.handle_node_creation_request)
        else:
            print("Error: NodeSearchPopup failed to initialize.")

        self.is_panning = False
        self.last_mouse_pos = None

    def search_popup_was_closed(self):
        """Callback for when the search popup signals it has been closed."""
        print("GraphView: Search popup was closed. Clearing reference.")
        self.search_popup = None

    def handle_node_creation_request(self, node_name: str, scene_pos: QPointF):
        if self.scene() and hasattr(self.scene(), 'controller') and self.scene().controller:
            self.scene().controller.create_node(node_name, scene_pos.x(), scene_pos.y())
        else:
            print("GraphView: Scene or controller no longer available for node creation.")

    def show_search_popup(self):
        if not self.search_popup:
            print("GraphView: Recreating search_popup.")
            if self.scene() and hasattr(self.scene(), 'controller'):
                self.search_popup = NodeSearchPopup(self.scene().controller, self)
                self.search_popup.node_selected.connect(self.handle_node_creation_request)
            else:
                print("GraphView: Cannot recreate search_popup, scene or controller missing.")
                return

        try:
            global_cursor_pos = self.cursor().pos()
            view_cursor_pos = self.mapFromGlobal(global_cursor_pos)
            if not self.viewport().rect().contains(view_cursor_pos):
                view_cursor_pos = self.viewport().rect().center()
        except Exception:
            view_cursor_pos = self.viewport().rect().center()

        if not self.search_popup: return

        self.search_popup.set_target_scene_pos(self.mapToScene(view_cursor_pos))
        self.search_popup.move(view_cursor_pos)
        self.search_popup.show_popup()

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            key_event = QKeyEvent(event)
            if key_event.key() == Qt.Key.Key_Tab:
                self.show_search_popup()
                return True
            elif key_event.key() == Qt.Key.Key_Escape:
                if self.search_popup and self.search_popup.isVisible():
                    temp_popup_ref = self.search_popup
                    temp_popup_ref.hide_popup()
                    return True
        return super().event(event)

    def mousePressEvent(self, event):
        self.setFocus()

        popup_handled_click = False
        if self.search_popup and self.search_popup.isVisible():
            try:
                popup_rect_in_view = self.search_popup.geometry()
                if not popup_rect_in_view.contains(event.pos()):
                    temp_popup_ref = self.search_popup
                    temp_popup_ref.hide_popup()
                    popup_handled_click = True
            except RuntimeError:
                print("GraphView.mousePressEvent: search_popup already deleted when checking bounds.")
                self.search_popup = None
                popup_handled_click = True

        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        elif not popup_handled_click:
            super().mousePressEvent(event)

    def wheelEvent(self, event):
        if not QApplication.instance(): return
        scale_factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        self.scale(scale_factor, scale_factor)

    def mouseMoveEvent(self, event):
        if not QApplication.instance(): return
        if self.is_panning and (event.buttons() & Qt.MouseButton.MiddleButton):
            delta_view = event.pos() - self.last_mouse_pos
            self.last_mouse_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta_view.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta_view.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if not QApplication.instance(): return
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def leaveEvent(self, event):
        if not QApplication.instance(): return
        if self.is_panning:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)

    def closeEvent(self, event):
        print("GraphView closing.")
        if self.search_popup:
            print("GraphView.closeEvent: Requesting search_popup deletion.")
            self.search_popup.deleteLater()
            self.search_popup = None
        super().closeEvent(event)