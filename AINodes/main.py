import os
import sys

from PySide6.QtWidgets import QApplication

from AINodes.src.core.node_editor import NodeEditor
from AINodes.src.nodes.basic.data.array_to_string_basic_node import ArrayToStringBasicNode
from AINodes.src.nodes.basic.data.data_split_node import DataSplitNode  # Import DataSplitNode
from AINodes.src.nodes.basic.data.float_to_string_basic_node import FloatToStringBasicNode
from AINodes.src.nodes.basic.math.add_and_multiply_basic_node import AddAndMultiplyBasicNode
from AINodes.src.nodes.basic.ml.lineare_regression_basic_node import LinearRegressionNode
from AINodes.src.nodes.basic.ml.r2_score_basic_node import R2ScoreBasicNode
from AINodes.src.nodes.input.single_float_input_node import SingleFloatInputNode
from AINodes.src.nodes.input.sklearn_dataset_input_node import SklearnDatasetInputNode
from AINodes.src.nodes.output.print_output_node import PrintOutputNode
from AINodes.src.ui.graphic_node import GraphicNode
from AINodes.src.ui.main_window import MainWindow

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Add current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))  # Add "src" folder to path


def test_sklearn_dataset():
    print("🔍 Testing SklearnDatasetInputNode...")

    # ✅ Only testing the working datasets
    datasets_to_test = ["iris", "wine", "california_housing"]

    for dataset_name in datasets_to_test:
        print(f"\n📂 Loading dataset: {dataset_name}")

        # Create dataset node
        dataset_node = SklearnDatasetInputNode(node_id=f"dataset_{dataset_name}", dataset_name=dataset_name)

        # Execute node to load data
        output = dataset_node.compute()

        if output is None:
            print(f"❌ Failed to load dataset: {dataset_name}")
            continue

        # Extract outputs
        dataset_dict = output.get("dataset_dict", {})
        features = output.get("features", [])
        targets = output.get("targets", [])

        # Print results
        print(
            f"✅ {dataset_name} - Features Shape: {len(features)} samples, {len(features[0]) if features else 0} features")
        print(f"✅ {dataset_name} - Targets Shape: {len(targets)} labels")
        print(f"🔹 Sample Features: {features[:3]}")
        print(f"🔹 Sample Targets: {targets[:10]}")
        print(f"🔹 Full Dataset Dict Keys: {list(dataset_dict.keys())}")


def test_multiply_add() -> None:
    """
    Tests the AddAndMultiplyBasicNode by performing addition and multiplication on two input values.
    - Uses fixed float input nodes.
    - Outputs the results via print nodes.
    """
    editor = NodeEditor()

    # Create nodes
    input_node_1 = editor.add_new_node("SingleFloatInputNode")
    #input_node_1 = SingleFloatInputNode("input_1", 10)
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
    """
    Constructs and executes a node-based machine learning pipeline using Linear Regression.
    - Loads dataset (e.g., Iris).
    - Splits dataset into train/test sets (90% train, 10% test).
    - Trains a Linear Regression model.
    - Computes R² score for model evaluation.
    - Outputs predictions and R² score.
    """
    editor = NodeEditor()

    # Load dataset
    dataset_node = SklearnDatasetInputNode("dataset_iris", dataset_name="iris")

    # Create data split node
    data_split_node = DataSplitNode("data_split", test_size=0.1, random_state=42)

    # Create Linear Regression node
    regression_node = LinearRegressionNode("linear_regression")

    # Create R² score node
    r2_score_node = R2ScoreBasicNode("r2_score")

    # Convert outputs to strings for display
    array_to_string_predictions = ArrayToStringBasicNode("array_to_string_predictions")
    float_to_string_r2 = FloatToStringBasicNode("float_to_string_r2")

    # Output nodes
    output_predictions = PrintOutputNode("output_predictions")
    output_r2 = PrintOutputNode("output_r2")

    # Connect dataset outputs to the split node inputs
    dataset_node.outputs[1].connect(data_split_node.inputs[0])  # Features → DataSplit
    dataset_node.outputs[2].connect(data_split_node.inputs[1])  # Targets → DataSplit

    # Connect train/test data to regression model
    data_split_node.outputs[0].connect(regression_node.inputs[0])  # X_train
    data_split_node.outputs[2].connect(regression_node.inputs[1])  # y_train
    data_split_node.outputs[1].connect(regression_node.inputs[2])  # X_test

    # Convert predictions to string before printing
    regression_node.outputs[1].connect(array_to_string_predictions.inputs[0])
    array_to_string_predictions.outputs[0].connect(output_predictions.inputs[0])

    # Compute and print R² score
    data_split_node.outputs[3].connect(r2_score_node.inputs[0])  # y_test
    regression_node.outputs[1].connect(r2_score_node.inputs[1])  # y_pred
    r2_score_node.outputs[0].connect(float_to_string_r2.inputs[0])
    float_to_string_r2.outputs[0].connect(output_r2.inputs[0])

    # Add nodes to editor
    editor.add_node(dataset_node)
    editor.add_node(data_split_node)
    editor.add_node(regression_node)
    editor.add_node(r2_score_node)
    editor.add_node(array_to_string_predictions)
    editor.add_node(float_to_string_r2)
    editor.add_node(output_predictions)
    editor.add_node(output_r2)

    # Execute nodes
    editor.execute_all()


def test_data_split_node():
    """
    Constructs and executes a node-based data processing pipeline using DataSplitNode.
    - Loads dataset (e.g., Iris).
    - Splits dataset into train/test sets (90% train, 10% test).
    - Converts arrays to strings before printing.
    """
    print("🔍 Testing DataSplitNode...")

    # Initialize Node Editor
    editor = NodeEditor()

    # Create dataset node (using Iris dataset)
    dataset_node = SklearnDatasetInputNode("dataset_iris", dataset_name="iris")

    # Create data split node
    data_split_node = DataSplitNode("data_split", test_size=0.1, random_state=42)

    # linear regression node

    regression_node = LinearRegressionNode("linear_regression")

    # create r2 score node

    r2_score_node = R2ScoreBasicNode("r2_score")

    # Create array-to-string conversion nodes
    array_to_string_X_train = ArrayToStringBasicNode("array_to_string_X_train")
    array_to_string_X_test = ArrayToStringBasicNode("array_to_string_X_test")
    array_to_string_y_train = ArrayToStringBasicNode("array_to_string_y_train")
    array_to_string_y_test = ArrayToStringBasicNode("array_to_string_y_test")
    array_to_string_predictions = ArrayToStringBasicNode("array_to_string_predictions")

    # Create float-to-string node for R² score
    float_to_string_r2 = FloatToStringBasicNode("float_to_string_r2")

    # Create print output nodes
    output_X_train = PrintOutputNode("output_X_train")
    output_X_test = PrintOutputNode("output_X_test")
    output_y_train = PrintOutputNode("output_y_train")
    output_y_test = PrintOutputNode("output_y_test")

    output_predictions = PrintOutputNode("output_predictions")
    output_r2_score = PrintOutputNode("output_r2_score")

    # Connect dataset outputs to the split node inputs
    dataset_node.outputs[1].connect(data_split_node.inputs[0])  # Features → DataSplit
    dataset_node.outputs[2].connect(data_split_node.inputs[1])  # Targets → DataSplit

    # Connect split outputs to the regression model
    data_split_node.outputs[0].connect(regression_node.inputs[0])  # X_train
    data_split_node.outputs[2].connect(regression_node.inputs[1])  # y_train
    data_split_node.outputs[1].connect(regression_node.inputs[2])  # X_test

    # Connect regression outputs
    regression_node.outputs[1].connect(array_to_string_predictions.inputs[0])  # Predictions → Convert

    # Connect regression predictions and y_test to R² score node
    data_split_node.outputs[3].connect(r2_score_node.inputs[0])  # y_test (true values)
    regression_node.outputs[1].connect(r2_score_node.inputs[1])  # Predictions

    # Convert R² score to string before printing
    r2_score_node.outputs[0].connect(float_to_string_r2.inputs[0])

    # Connect outputs to print nodes
    editor.connect_sockets(data_split_node.outputs[0], array_to_string_X_train.inputs[0])
    #data_split_node.outputs[0].connect(array_to_string_X_train.inputs[0])  # X_train → Convert
    data_split_node.outputs[1].connect(array_to_string_X_test.inputs[0])  # X_test → Convert
    data_split_node.outputs[2].connect(array_to_string_y_train.inputs[0])  # y_train → Convert
    data_split_node.outputs[3].connect(array_to_string_y_test.inputs[0])  # y_test → Convert

    # Connect converted strings to print nodes
    array_to_string_X_train.outputs[0].connect(output_X_train.inputs[0])
    array_to_string_X_test.outputs[0].connect(output_X_test.inputs[0])
    array_to_string_y_train.outputs[0].connect(output_y_train.inputs[0])
    array_to_string_y_test.outputs[0].connect(output_y_test.inputs[0])
    array_to_string_predictions.outputs[0].connect(output_predictions.inputs[0])
    float_to_string_r2.outputs[0].connect(output_r2_score.inputs[0])

    # Add nodes to the editor
    editor.add_node(dataset_node)
    editor.add_node(data_split_node)
    editor.add_node(regression_node)
    editor.add_node(r2_score_node)
    editor.add_node(array_to_string_X_train)
    editor.add_node(array_to_string_X_test)
    editor.add_node(array_to_string_y_train)
    editor.add_node(array_to_string_y_test)
    editor.add_node(array_to_string_predictions)
    editor.add_node(float_to_string_r2)
    editor.add_node(output_X_train)
    editor.add_node(output_X_test)
    editor.add_node(output_y_train)
    editor.add_node(output_y_test)
    editor.add_node(output_predictions)
    editor.add_node(output_r2_score)

    # Execute the pipeline
    editor.execute_all()


def test_ui():
    app = QApplication([])
    editor = MainWindow()
    editor.show()

    # node1 = GraphicNode("Standard Node", x=0, y=0, num_inputs=5, num_outputs=2)
    # node2 = GraphicNode("Input Node", x=-200, y=0, num_inputs=0, num_outputs=2)
    # node3 = GraphicNode("Output Node", x=200, y=0, num_inputs=2, num_outputs=0)
    #
    # editor.scene.addItem(node1)
    # editor.scene.addItem(node2)
    # editor.scene.addItem(node3)

    app.exec()

if __name__ == "__main__":
    # UI-related code (commented out)
    # print(a)
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec())

    # Execute backend node-based system
    # main()
    # Run the test
    # test_sklearn_dataset()
    # Run the test
    # test_data_split_node()
    test_ui()
    # test_multiply_add()




