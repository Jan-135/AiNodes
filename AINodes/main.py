import os
import sys

from PySide6.QtWidgets import QApplication

from AINodes.src.core.node_editor import NodeEditor
from AINodes.src.nodes.basic.add_basic_node import AddBasicNode
from AINodes.src.nodes.input.single_float_input_node import SingleFloatInputNode
from AINodes.src.nodes.output.print_output_node import PrintOutputNode
from AINodes.src.ui.main_window import MainWindow

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Fügt das aktuelle Verzeichnis hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))  # Fügt den src-Ordner hinzu


def main():
    editor = NodeEditor()

    # Create nodes
    input_node1 = SingleFloatInputNode("input_1", value=22.0)
    input_node2 = SingleFloatInputNode("input_2", value=42.0)

    add_node = AddBasicNode("add_1")

    output_node = PrintOutputNode("output_1")

    # Add nodes to editor
    editor.add_node(output_node)
    editor.add_node(input_node1)
    editor.add_node(input_node2)
    editor.add_node(add_node)


    # Connect sockets directly
    input_node1.outputs[0].connect(add_node.inputs[0])
    input_node2.outputs[0].connect(add_node.inputs[1])
    add_node.outputs[0].connect(output_node.inputs[0])

    # Execute all nodes
    editor.execute_all()


if __name__ == "__main__":
    # Grafischer Code


    # print(a)
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec())

  #  BackEnd Code
   # Erstellt eine Instanz des NodeEditors
    main()
