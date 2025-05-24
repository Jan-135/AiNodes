from pathlib import Path

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QBrush, QColor, QPen, QPainterPath, QTextOption, QPainter, QPalette
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsDropShadowEffect, \
    QDoubleSpinBox, QComboBox, QLineEdit, QGraphicsProxyWidget, QStyleOptionGraphicsItem, QWidget

from AINodes.src.core.node import Node
from AINodes.src.sockets.socket import Socket
from AINodes.src.ui.graphic_socket import GraphicSocket



class GraphicNode(QGraphicsItem):
    def __init__(self, parent: Node = None, x=0, y=0):
        super().__init__()
        if parent is None:
            raise ValueError("GraphicNode requires a valid parent Node object.")

        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

        self.node = parent
        self.node_type = parent.node_type
        self.node_id = parent.node_id

        # --- Configuration ---
        self.width = 180
        self.title_height = 25
        self.vertical_spacing = 30
        self.padding = 10
        self.socket_radius = 5
        self.horizontal_padding = 10
        self.label_socket_spacing = 8

        # --- Calculate Required Height (Outputs + Inputs + Parameters) ---
        self.num_inputs = len(parent.inputs)
        self.num_outputs = len(parent.outputs)
        # *** CHANGED: Total rows needed for sockets is the SUM ***
        socket_rows = self.num_outputs + self.num_inputs
        socket_section_height = (socket_rows * self.vertical_spacing) + self.padding if socket_rows > 0 else 0

        self.parameters = {}
        self.parameter_widgets = []
        self.num_params = 0
        parameter_section_height = 0
        if hasattr(parent, "serialize_parameters"):
            self.parameters = parent.serialize_parameters()
            self.num_params = len(self.parameters)
            if self.num_params > 0:
                 parameter_section_height = (self.num_params * self.vertical_spacing) + self.padding

        # *** CHANGED: Recalculate total height based on sequential layout ***
        self.body_height = socket_section_height + parameter_section_height
        self.total_height = self.title_height + self.body_height

        # --- Define Node Geometry (Using updated height) ---
        # *** CHANGED: Geometry uses updated height ***
        self.node_rect = QRectF(-self.width / 2, -self.total_height / 2, self.width, self.total_height)
        self.title_rect = QRectF(-self.width / 2, -self.total_height / 2, self.width, self.title_height)
        self.body_rect = QRectF(-self.width / 2, self.title_rect.bottom(), self.width, self.body_height)

        # --- Create Child Items (Sockets, Labels, Parameter Widgets) ---
        self.sockets = []
        self.socket_labels = []

        # Y offset for first row of content within the body
        content_start_y = self.body_rect.top() + self.padding / 2

        # --- Track the current vertical row index across both loops ---
        # *** ADDED: Row tracker ***
        current_row_index = 0

        # --- Output Sockets and Labels (Placed FIRST) ---
        # *** CHANGED: Loop order and Y calculation ***
        for i in range(self.num_outputs):
            # Calculate vertical center for THIS row using current_row_index
            row_center_y = content_start_y + (current_row_index * self.vertical_spacing) + (self.vertical_spacing / 2)
            socket_id = parent.outputs[i].socket_id

            # --- X calculation remains UNCHANGED from your provided code ---
            socket_center_x = self.width / 2 - self.horizontal_padding - self.socket_radius + 15
            # Create socket using correct X and NEW Y
            socket = GraphicSocket(socket_id, socket_center_x, row_center_y, self, is_input=False)
            self.sockets.append(socket)

            # Create Output Label
            label = QGraphicsTextItem(parent.outputs[i].socket_name, self)
            label.setDefaultTextColor(Qt.GlobalColor.white)
            label_height = label.boundingRect().height()
            label_width = label.boundingRect().width()
            # Calculate label's TOP Y using NEW row_center_y
            label_top_y = row_center_y - (label_height / 2)
            # --- Label X calculation remains UNCHANGED from your provided code ---
            socket_left_edge = socket_center_x - self.socket_radius
            label_right_x = socket_left_edge - self.label_socket_spacing
            label_left_x = label_right_x - label_width
            # Set label position with UNCHANGED X and NEW Y
            label.setPos(label_left_x, label_top_y)
            self.socket_labels.append(label)

            # Increment row index for the next item
            current_row_index += 1

        # --- Input Sockets and Labels (Placed AFTER Outputs) ---
        # *** CHANGED: Y calculation ***
        for i in range(self.num_inputs):
            # Calculate vertical center using the *updated* current_row_index
            row_center_y = content_start_y + (current_row_index * self.vertical_spacing) + (self.vertical_spacing / 2)
            socket_id = parent.inputs[i].socket_id

            # --- X calculation remains UNCHANGED from your provided code ---
            socket_center_x = -self.width / 2 + self.horizontal_padding + self.socket_radius - 15
            # Create socket using correct X and NEW Y
            socket = GraphicSocket(socket_id, socket_center_x, row_center_y, self, is_input=True)
            self.sockets.append(socket)

            # Create Input Label
            label = QGraphicsTextItem(parent.inputs[i].socket_name, self)
            label.setDefaultTextColor(Qt.GlobalColor.white)
            label_height = label.boundingRect().height()
            # Calculate label's TOP Y using NEW row_center_y
            label_top_y = row_center_y - (label_height / 2)
            # --- Label X calculation remains UNCHANGED from your provided code ---
            socket_right_edge = socket_center_x + self.socket_radius
            label_left_x = socket_right_edge + self.label_socket_spacing
            # Set label position with UNCHANGED X and NEW Y
            label.setPos(label_left_x, label_top_y)
            self.socket_labels.append(label)

            # Increment row index
            current_row_index += 1


        # --- Create Parameter Widgets (Positioned below ALL sockets) ---
        # *** CHANGED: param_start_y calculation uses updated socket_section_height ***
        param_start_y = self.body_rect.top() + socket_section_height + self.padding / 2
        self.create_parameter_widgets(param_start_y)  # Pass correct starting Y

        # --- Effects ---
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

    # --- Other methods (boundingRect, paint, itemChange) remain the same as before ---
    def boundingRect(self) -> QRectF:
        extra = 5
        return self.node_rect.adjusted(-extra, -extra, extra, extra)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = None) -> None:
        # --- Configuration ---
        radius = 8.0 # Adjust this value for desired roundness (e.g., 8.0 or your previous 20.0)

        # --- 1. Define the Overall Rounded Shape ---
        # Use addRoundedRect for a reliable rounded rectangle path.
        full_node_path = QPainterPath()
        full_node_path.addRoundedRect(self.node_rect, radius, radius)

        # --- 2. Draw Backgrounds using Clipping ---
        painter.save() # Save painter state before clipping

        # Set the clip region to the rounded path. Everything drawn
        # after this will be confined within this shape.
        painter.setClipPath(full_node_path)

        # Draw the main body background (fills the entire clipped area)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(48, 48, 48))) # Dark grey body
        # Use drawPath to ensure filling exactly the clipped rounded shape
        painter.drawPath(full_node_path)

        # Draw the title background rectangle. Because of the clip path,
        # only the portion within the rounded node shape (including the
        # rounded top corners) will be visible.
        painter.setBrush(QBrush(QColor(60, 120, 100))) # Green title
        # Draw the rectangular title area; clipping handles the shape.
        painter.drawRect(self.title_rect)

        painter.restore() # Restore painter state (removes clipping)

        # --- 3. Draw Node Outline ---
        # Draw the outline using the same rounded path AFTER restoring
        # from the clip, so the outline itself isn't clipped.
        painter.setPen(QPen(QColor(20, 20, 20), 1)) # Subtle outline color
        painter.setBrush(Qt.BrushStyle.NoBrush) # No fill for the outline
        painter.drawPath(full_node_path)

        # --- 4. Draw Title Text ---
        painter.setPen(QColor(255, 255, 255)) # White text
        painter.drawText(self.title_rect, Qt.AlignmentFlag.AlignCenter, self.node_type)

        # --- 5. Draw Selection Highlight ---
        if self.isSelected():
            pen = QPen(QColor(255, 255, 255), 1)  # Use a distinct selection color (e.g., yellow)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            # Draw the highlight slightly inside the main outline for better visibility
            # Adjusting the original path or creating a slightly smaller rounded rect
            # For simplicity, let's draw the highlight using the same full path but with the selection pen
            # Or draw a rectangle slightly inset:
            inset = 0  # Amount to inset the selection rectangle
            selection_rect = self.node_rect.adjusted(inset, inset, -inset, -inset)
            # To draw a rounded rectangle highlight easily:
            painter.drawRoundedRect(selection_rect, radius - inset, radius - inset)  # Use slightly smaller radius
            # If you prefer a sharp rectangle selection:
            # painter.drawRect(selection_rect)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value) -> QGraphicsItem | QPointF | None:
        # Use ItemPositionHasChanged for efficiency after move completes
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for socket in self.sockets:
                # Crude way to access connections - refine if possible
                for connection in getattr(socket, "connections", []):
                    # Ensure connection object has this method
                    if hasattr(connection, 'update_position'):
                        connection.update_position()
        return super().itemChange(change, value)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value) -> QGraphicsItem | QPointF | None:
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:  # Use ItemPositionHasChanged for efficiency
            # print(f"Node {self.node_id} moved")
            for socket in self.sockets:
                # Assuming connections are stored on sockets and have an update_position method
                for connection in getattr(socket, "connections", []):
                    # print(f"Updating connection for socket {socket.socket_id}")
                    connection.update_position()
        return super().itemChange(change, value)

    def create_parameter_widgets(self, start_y: float):
        if not self.parameters:
            return  # Nothing to create

        # Available width for label + widget within the node body, considering padding
        available_content_width = self.width - 2 * self.padding
        label_width_ratio = 0.4  # Allocate 40% width to label
        widget_width_ratio = 0.55  # Allocate 55% width to widget
        spacing_ratio = 0.05  # Allocate 5% width to spacing

        for i, (key, value) in enumerate(self.parameters.items()):
            # Calculate vertical center for this parameter row
            current_row_y = start_y + (i * self.vertical_spacing) + (self.vertical_spacing / 2)

            # --- Label for the parameter ---
            param_label_text = f"{key}:"
            param_label = QGraphicsTextItem(param_label_text, self)
            param_label.setDefaultTextColor(Qt.GlobalColor.white)
            # Position label left-aligned
            label_max_width = available_content_width * label_width_ratio
            param_label.setTextWidth(label_max_width)  # Limit label width if needed

            label_height = param_label.boundingRect().height()
            label_top_y = current_row_y - (label_height / 2)  # Center vertically
            label_left_x = -self.width / 2 + self.padding  # Align with left padding
            param_label.setPos(label_left_x, label_top_y)
            self.socket_labels.append(param_label)  # Add to general labels list

            # --- Actual Widget ---
            widget_instance = None  # Store the actual QWidget

            # Determine widget type based on value type (and key for specifics)
            if isinstance(value, (float, int)):
                widget_instance = QDoubleSpinBox()
                widget_instance.setValue(float(value))
                widget_instance.setRange(-999999, 999999)
                widget_instance.setSingleStep(0.1 if isinstance(value, float) else 1.0)
                widget_instance.setDecimals(4 if isinstance(value, float) else 0)  # Adjust precision
                # widget_instance.setAlignment(Qt.AlignmentFlag.AlignRight)
                widget_instance.valueChanged.connect(lambda val, k=key: self._update_node_param(k, val))

                widget_instance.setStyleSheet("""
                    QDoubleSpinBox {
                        background-color: #303030;
                        border: 1px solid #5e5e5e;
                        color: white;
                        padding: 2px;
                        border-radius: 4px;
                    }
                    
                    QDoubleSpinBox::down-button {
                        image: url(C:/Users/Jan/source/repos/AINodes/AINodes/src/ui/icons/keyboard_arrow_down.svg);
                        background-color: #222;
                        border: None;
                        width: 20px;
                        border-bottom-right-radius: 3px;
                        border-top: 1px solid #5e5e5e;
                        border-left: 1px solid #5e5e5e;
                        image-rendering: auto;
                    }
                    QDoubleSpinBox::up-button {
                        image: url(C:/Users/Jan/source/repos/AINodes/AINodes/src/ui/icons/keyboard_arrow_up.svg);
                        background-color: #222;
                        border: None;
                        width: 20px;
                        border-top-right-radius: 3px;
                        border-left: 1px solid #5e5e5e;
                        image-rendering: auto;
                        


                    }
                    
                    QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
                        background-color: #3a3a3a;
                    }
                """)

            elif isinstance(value, str) and key == "dataset_name" and hasattr(self.node, "AVAILABLE_DATASETS"):
                widget_instance = QComboBox()
                datasets = getattr(self.node, "AVAILABLE_DATASETS", {})
                if isinstance(datasets, dict):
                    widget_instance.addItems(list(datasets.keys()))
                else:
                    widget_instance.addItems(list(datasets))
                widget_instance.setCurrentText(value)
                widget_instance.currentTextChanged.connect(lambda val, k=key: self._update_node_param(k, val))

            elif isinstance(value, str):
                widget_instance = QLineEdit()
                widget_instance.setText(value)
                widget_instance.textChanged.connect(lambda val, k=key: self._update_node_param(k, val))

            elif isinstance(value, bool):
                from PySide6.QtWidgets import QCheckBox  # Import locally if not already imported
                widget_instance = QCheckBox()
                widget_instance.setChecked(value)
                widget_instance.toggled.connect(lambda val, k=key: self._update_node_param(k, val))

            # Add more elif conditions for other types...

            if widget_instance:
                # Set widget size
                widget_max_width = available_content_width * widget_width_ratio
                widget_instance.setFixedWidth(widget_max_width)
                widget_instance.setFixedHeight(self.vertical_spacing * 0.8)  # Slightly less than row height

                # Wrap widget in proxy
                proxy = QGraphicsProxyWidget(self)
                proxy.setWidget(widget_instance)

                # Position proxy widget (right-aligned in the remaining space)
                widget_left_x = self.width / 2 - self.padding - widget_max_width
                widget_top_y = current_row_y - (widget_instance.height() / 2)  # Center vertically

                proxy.setPos(widget_left_x, widget_top_y)
                proxy = QGraphicsProxyWidget(self)
                proxy.setWidget(widget_instance)

                # --- ADD THIS LINE ---
                proxy.setCacheMode(QGraphicsItem.CacheMode.NoCache)
                # ---------------------

                # ... (Position proxy widget) ...
                self.parameter_widgets.append(proxy)

    def _update_node_param(self, key: str, value):
        if hasattr(self.node, key):
            try:

                current_value = getattr(self.node, key)
                value_type = type(current_value)
                if value_type is int and isinstance(value, float):
                    value = int(value)
                if value_type is float and isinstance(value, int):
                    value = float(value)

                setattr(self.node, key, value)
            except Exception as e:
                print(f"Error updating parameter {key}: {e}")
        else:
            print(f"No parameter key {key} in node {self.node}")
