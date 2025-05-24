from PySide6.QtWidgets import (QLineEdit, QListWidget, QListWidgetItem,
                               QWidget, QVBoxLayout, QApplication, QFrame)
from PySide6.QtCore import Qt, QPointF, Signal, QEvent, QObject
from PySide6.QtGui import QKeyEvent


class NodeSearchPopup(QWidget):
    node_selected = Signal(str, QPointF)

    def __init__(self, controller, parent_view):
        super().__init__(parent_view)
        self.controller = controller
        self.parent_view = parent_view

        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setMinimumWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Search Nodes...")
        layout.addWidget(self.line_edit)

        self.list_widget = QListWidget()
        self.list_widget.setVisible(False)
        self.list_widget.setMaximumHeight(150)
        layout.addWidget(self.list_widget)

        self.all_node_names = list(controller.get_available_nodes().keys())
        self._target_scene_pos = QPointF(0, 0)

        self.line_edit.textChanged.connect(self.filter_and_show_list)
        self.line_edit.returnPressed.connect(self.on_line_edit_return_pressed)
        self.list_widget.itemClicked.connect(self.on_list_item_clicked)
        self.list_widget.itemActivated.connect(self.on_list_item_activated)

        self.line_edit.installEventFilter(self)
        self.list_widget.installEventFilter(self)
        self.installEventFilter(self)

    def set_target_scene_pos(self, scene_pos: QPointF):
        self._target_scene_pos = scene_pos

    def show_popup(self):
        self.line_edit.clear()
        self.list_widget.clear()
        self.list_widget.setVisible(False)
        self.show()
        self.raise_()
        self.line_edit.setFocus()
        self.filter_and_show_list("")
        self.adjustSize()

    def filter_and_show_list(self, text: str):
        self.list_widget.clear()
        has_matches = False
        if not text.strip():
            for name in self.all_node_names:
                self.list_widget.addItem(QListWidgetItem(name))
            has_matches = len(self.all_node_names) > 0
        else:
            for name in self.all_node_names:
                if text.lower() in name.lower():
                    self.list_widget.addItem(QListWidgetItem(name))
                    has_matches = True

        if has_matches:
            if not self.list_widget.isVisible():
                self.list_widget.setVisible(True)
            self.list_widget.setCurrentRow(0)
        else:
            self.list_widget.setVisible(False)
        self.adjustSize()

    def on_line_edit_return_pressed(self):
        if self.list_widget.isVisible() and self.list_widget.currentItem():
            selected_node_name = self.list_widget.currentItem().text()
        else:
            text = self.line_edit.text()
            direct_match = next((name for name in self.all_node_names if name.lower() == text.lower()), None)
            if direct_match:
                selected_node_name = direct_match
            elif self.list_widget.count() > 0:
                self.list_widget.setCurrentRow(0)
                selected_node_name = self.list_widget.currentItem().text()
            else:
                self.hide_popup()
                return
        self.create_selected_node(selected_node_name)

    def on_list_item_clicked(self, item: QListWidgetItem):
        self.create_selected_node(item.text())

    def on_list_item_activated(self, item: QListWidgetItem):
        self.create_selected_node(item.text())

    def create_selected_node(self, node_name: str):
        self.node_selected.emit(node_name, self._target_scene_pos)
        self.hide_popup()

    def hide_popup(self):
        parent_view_ref = self.parent_view
        is_visible_before_hide = self.isVisible()

        self.hide()

        if parent_view_ref and is_visible_before_hide:
            parent_view_ref.setFocus()
            if hasattr(parent_view_ref, 'search_popup_was_closed'):
                parent_view_ref.search_popup_was_closed()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            key_event = QKeyEvent(event)

            if key_event.key() == Qt.Key.Key_Escape:
                self.hide_popup()
                return True

            if watched == self.line_edit:
                if key_event.key() == Qt.Key.Key_Down:
                    if self.list_widget.isVisible() and self.list_widget.count() > 0:
                        self.list_widget.setFocus()
                        if self.list_widget.currentRow() < 0:
                            self.list_widget.setCurrentRow(0)
                    return True
            elif watched == self.list_widget:
                if key_event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                    if self.list_widget.currentItem():
                        self.create_selected_node(self.list_widget.currentItem().text())
                    return True
                elif key_event.key() == Qt.Key.Key_Up and self.list_widget.currentRow() == 0:
                    self.line_edit.setFocus()
                    return True
            elif watched == self and key_event.key() == Qt.Key.Key_Escape:
                self.hide_popup()
                return True

        if event.type() == QEvent.Type.WindowDeactivate and self.isVisible():
            pass

        return super().eventFilter(watched, event)

    def closeEvent(self, event):
        print(f"NodeSearchPopup ({id(self)}) closeEvent triggered.")
        if self.parent_view and self.isVisible():
            self.parent_view.setFocus()
            if hasattr(self.parent_view, 'search_popup_was_closed'):
                self.parent_view.search_popup_was_closed()
        super().closeEvent(event)
