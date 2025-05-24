# file: AINodes/src/ui/node_search_popup.py
from PySide6.QtWidgets import (QLineEdit, QListWidget, QGraphicsProxyWidget, QListWidgetItem,
                               QWidget, QVBoxLayout, QApplication) # Added QWidget, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, QPointF, Signal, QEvent, QObject
from PySide6.QtGui import QKeyEvent # Added QKeyEvent

class NodeSearchPopup(QGraphicsProxyWidget):
    node_selected = Signal(str, QPointF) # Signal to emit node name and position

    def __init__(self, controller, scene_view): # Pass scene_view instead of scene
        super().__init__()
        self.controller = controller
        self.scene_view = scene_view # Store the view

        # --- Main widget to hold line_edit and list_widget ---
        self.main_widget = QWidget()
        self.main_widget.setMinimumWidth(200) # Set a reasonable minimum width
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(0, 0, 0, 0) # No extra margins
        layout.setSpacing(0) # No spacing between line edit and list

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Search Nodes...")
        layout.addWidget(self.line_edit)

        self.list_widget = QListWidget()
        self.list_widget.setVisible(False) # Initially hidden
        self.list_widget.setMaximumHeight(150) # Limit height to prevent being too tall
        layout.addWidget(self.list_widget)

        self.main_widget.setLayout(layout)
        self.setWidget(self.main_widget)
        self.setZValue(1000)  # Ensure it's on top
        self.setVisible(False) # Initially hidden

        self.all_node_names = list(controller.get_available_nodes().keys()) # Store all available node names

        # --- Connections ---
        self.line_edit.textChanged.connect(self.filter_and_show_list)
        self.line_edit.returnPressed.connect(self.on_line_edit_return_pressed)
        self.list_widget.itemClicked.connect(self.on_list_item_clicked)
        # Or use itemActivated for double-click or Enter on a list item
        self.list_widget.itemActivated.connect(self.on_list_item_activated)

        # --- Event Filter for Keyboard Navigation ---
        self.line_edit.installEventFilter(self)
        self.list_widget.installEventFilter(self)
        self.current_scene_pos = QPointF(0,0)


    def show_at(self, scene_pos: QPointF):
        self.current_scene_pos = scene_pos # Store the position for node creation
        self.setPos(scene_pos)
        self.line_edit.clear()
        self.list_widget.clear()
        self.list_widget.setVisible(False) # Hide list initially
        self.setVisible(True)
        self.line_edit.setFocus()
        # Initial population without filter
        self.filter_and_show_list("")


    def filter_and_show_list(self, text: str):
        self.list_widget.clear()
        has_matches = False
        if not text.strip(): # If text is empty, show all or a limited number
            for name in self.all_node_names:
                self.list_widget.addItem(QListWidgetItem(name))
            has_matches = len(self.all_node_names) > 0
        else:
            for name in self.all_node_names:
                if text.lower() in name.lower():
                    self.list_widget.addItem(QListWidgetItem(name))
                    has_matches = True

        if has_matches:
            self.list_widget.setVisible(True)
            self.list_widget.setCurrentRow(0) # Select the first item by default
        else:
            self.list_widget.setVisible(False)
        self.adjust_size()

    def adjust_size(self):
        # Adjust the size of the proxy widget to fit its content
        self.widget().adjustSize()
        self.setGeometry(self.geometry().x(), self.geometry().y(),
                         self.widget().sizeHint().width(), self.widget().sizeHint().height())


    def on_line_edit_return_pressed(self):
        if self.list_widget.isVisible() and self.list_widget.currentItem():
            selected_node_name = self.list_widget.currentItem().text()
        else:
            # If list is not visible or no item selected, try to match line_edit text
            # This allows typing a full name and hitting enter
            text = self.line_edit.text()
            if text in self.all_node_names:
                selected_node_name = text
            else: # No valid selection
                self.hide_popup()
                return

        self.create_selected_node(selected_node_name)

    def on_list_item_clicked(self, item: QListWidgetItem):
        self.create_selected_node(item.text())

    def on_list_item_activated(self, item: QListWidgetItem): # For Enter/Double-click on list
        self.create_selected_node(item.text())

    def create_selected_node(self, node_name: str):
        self.node_selected.emit(node_name, self.current_scene_pos) # Emit signal
        self.hide_popup()

    def hide_popup(self):
        self.setVisible(False)
        self.line_edit.clear()
        self.list_widget.clear()
        self.list_widget.setVisible(False)
        # Return focus to the scene/view
        if self.scene_view:
            self.scene_view.setFocus()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            key_event = QKeyEvent(event) # Cast to QKeyEvent
            if watched == self.line_edit:
                if key_event.key() == Qt.Key.Key_Down:
                    if self.list_widget.isVisible() and self.list_widget.count() > 0:
                        self.list_widget.setFocus()
                        self.list_widget.setCurrentRow(0)
                    return True # Event handled
                elif key_event.key() == Qt.Key.Key_Escape:
                    self.hide_popup()
                    return True
            elif watched == self.list_widget:
                if key_event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                    if self.list_widget.currentItem():
                        self.create_selected_node(self.list_widget.currentItem().text())
                    return True # Event handled
                elif key_event.key() == Qt.Key.Key_Escape:
                    self.hide_popup()
                    return True
                elif key_event.key() == Qt.Key.Key_Up and self.list_widget.currentRow() == 0:
                    self.line_edit.setFocus() # Move focus back to line edit
                    return True

        return super().eventFilter(watched, event)