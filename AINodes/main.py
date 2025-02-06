import os
import sys


from AINodes.src.backend.node_editor import NodeEditor
from AINodes.src.backend.NodeLibrary.single_float_input_node import SingleFloatInputNode
from AINodes.src.backend.NodeLibrary.print_output_node import PrintOutputNode

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Fügt das aktuelle Verzeichnis hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))  # Fügt den src-Ordner hinzu


def main():
    editor = NodeEditor()

    # Create nodes
    input_node = SingleFloatInputNode("input_1", value=42.0)
    output_node = PrintOutputNode("output_1")

    # Add nodes to editor
    editor.add_node(output_node)
    editor.add_node(input_node)


    # Connect sockets directly
    input_node.outputs[0].connect(output_node.inputs[0])

    # Execute all nodes
    editor.execute_all()


if __name__ == "__main__":
    # Grafischer Code
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec())

    # BackEnd Code
    # Erstellt eine Instanz des NodeEditors
    main()
