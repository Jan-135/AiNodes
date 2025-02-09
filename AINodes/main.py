import os
import sys

from AINodes.src.core.node_editor import NodeEditor
from AINodes.src.nodes.basic.add_and_multiply_basic_node import AddAndMultiplyBasicNode
from AINodes.src.nodes.basic.array_to_string_basic_node import ArrayToStringBasicNode
from AINodes.src.nodes.basic.build_array_basic_node import BuildArrayBasicNode
from AINodes.src.nodes.basic.float_to_string_basic_node import FloatToStringBasicNode
from AINodes.src.nodes.basic.lineare_regression_basic_node import LinearRegressionNode
from AINodes.src.nodes.basic.r2_score_basic_node import R2ScoreBasicNode
from AINodes.src.nodes.input.single_float_input_node import SingleFloatInputNode
from AINodes.src.nodes.input.single_random_value_input_node import SingleRandomValueInputNode
from AINodes.src.nodes.output.print_output_node import PrintOutputNode

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Fügt das aktuelle Verzeichnis hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))  # Fügt den src-Ordner hinzu


def test_multiply_add():
    editor = NodeEditor()

    # Create nodes
    input_node_1 = SingleFloatInputNode("input_1", 10)
    input_node_2 = SingleFloatInputNode("input_2", 10)
    process_node = AddAndMultiplyBasicNode("process")
    output_node_1 = PrintOutputNode("output_1")
    output_node_2 = PrintOutputNode("output_2")

    # Connect nodes
    input_node_1.outputs[0].connect(process_node.inputs[0])
    input_node_2.outputs[0].connect(process_node.inputs[1])
    process_node.outputs[0].connect(output_node_1.inputs[0])
    process_node.outputs[1].connect(output_node_2.inputs[0])

    # Add nodes to editor
    editor.add_node(input_node_1)
    editor.add_node(input_node_2)
    editor.add_node(process_node)
    editor.add_node(output_node_1)
    editor.add_node(output_node_2)

    # Execute nodes
    editor.execute_all()


def main():
    editor = NodeEditor()

    # Erstelle Nodes
    x_train_node = BuildArrayBasicNode("x_train_builder")
    y_train_node = BuildArrayBasicNode("y_train_builder")
    x_test_node = BuildArrayBasicNode("x_test_builder")
    regression_node = LinearRegressionNode("linear_regression")
    output_node = PrintOutputNode("output_regression")
    r2_score_node = R2ScoreBasicNode("r2_score")  # Neue Node für R²-Wert
    float_to_string_node = FloatToStringBasicNode("float_to_string")

    # Zufällige Werte für Trainingsdaten generieren
    random_x_train = SingleRandomValueInputNode("random_x_train", min_value=1, max_value=10)
    random_y_train = SingleRandomValueInputNode("random_y_train", min_value=10, max_value=20)
    random_x_test = SingleRandomValueInputNode("random_x_test", min_value=1, max_value=10)
    length_node = SingleFloatInputNode("length", 5)  # Länge der Arrays

    array_to_string = ArrayToStringBasicNode("array_to_string")
    output_r2 = PrintOutputNode("output_r2")

    # Verbinde Nodes
    random_x_train.outputs[0].connect(x_train_node.inputs[0])
    length_node.outputs[0].connect(x_train_node.inputs[1])
    random_y_train.outputs[0].connect(y_train_node.inputs[0])
    length_node.outputs[0].connect(y_train_node.inputs[1])
    random_x_test.outputs[0].connect(x_test_node.inputs[0])
    length_node.outputs[0].connect(x_test_node.inputs[1])

    x_train_node.outputs[0].connect(regression_node.inputs[0])  # X_train
    y_train_node.outputs[0].connect(regression_node.inputs[1])  # y_train
    x_test_node.outputs[0].connect(regression_node.inputs[2])  # X_test

    regression_node.outputs[1].connect(array_to_string.inputs[0])  # Vorhersagen → String
    array_to_string.outputs[0].connect(output_node.inputs[0])  # String → Print Output

    # Verbindung zur R²-Node mit Float zu String Umwandlung
    y_train_node.outputs[0].connect(r2_score_node.inputs[0])  # y_true
    regression_node.outputs[1].connect(r2_score_node.inputs[1])  # y_pred
    r2_score_node.outputs[0].connect(float_to_string_node.inputs[0])
    float_to_string_node.outputs[0].connect(output_r2.inputs[0])

    # Füge Nodes dem Editor hinzu
    editor.add_node(random_x_train)
    editor.add_node(random_y_train)
    editor.add_node(random_x_test)
    editor.add_node(length_node)
    editor.add_node(x_train_node)
    editor.add_node(y_train_node)
    editor.add_node(x_test_node)
    editor.add_node(regression_node)
    editor.add_node(array_to_string)
    editor.add_node(output_node)
    editor.add_node(r2_score_node)
    editor.add_node(float_to_string_node)
    editor.add_node(output_r2)

    # Führe Nodes aus
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
