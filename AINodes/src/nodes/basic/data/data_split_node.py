import numpy as np
from sklearn.model_selection import train_test_split

from AINodes.src.core.basic_node import BasicNode


class DataSplitNode(BasicNode):
    """
    A node that splits input data into training and testing sets.
    - Takes in features (`X`) and target labels (`y`).
    - Accepts an optional random seed input.
    - Outputs `X_train`, `X_test`, `y_train`, `y_test`, and `random_state`.
    """

    def __init__(self, node_id: str, test_size: float = 0.1, random_state: int = 42):
        """
        Initializes the DataSplitNode.

        :param node_id: Unique identifier for the node.
        :param test_size: Proportion of data to be used for testing (default: 10%).
        :param random_state: Default random state if no input is connected.
        """
        super().__init__(node_id)
        self.test_size = test_size
        self.default_random_state = random_state  # Default seed

        # Input Sockets
        self.input_X = self.add_socket("input", "array", "features")  # Feature matrix
        self.input_y = self.add_socket("input", "array", "targets")  # Labels
        self.input_random_state = self.add_socket("input", "int", "random_seed")  # New input!

        # Output Sockets
        self.output_X_train = self.add_socket("output", "array", "X_train")
        self.output_X_test = self.add_socket("output", "array", "X_test")
        self.output_y_train = self.add_socket("output", "array", "y_train")
        self.output_y_test = self.add_socket("output", "array", "y_test")
        self.output_random_state = self.add_socket("output", "int", "random_state")  # New output!

    def compute(self):
        """
        Splits the dataset into training and testing sets.

        :return: A dictionary with `X_train`, `X_test`, `y_train`, `y_test`, and `random_state`.
        """
        X = self.input_X.pass_data()
        y = self.input_y.pass_data()
        random_seed = self.input_random_state.pass_data()  # Get seed from input

        if X is None or y is None:
            print("⚠ Missing input data for DataSplitNode.")
            return None

        # Use the provided seed or fall back to the default
        random_state = random_seed if random_seed is not None else self.default_random_state

        # Convert to NumPy arrays
        X = np.array(X)
        y = np.array(y)

        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=random_state
        )

        print(f"X_train size: {len(X_train)}, X_test size: {len(X_test)}")
        print(f"y_train size: {len(y_train)}, y_test size: {len(y_test)}")

        return {
            "X_train": X_train.tolist(),
            "X_test": X_test.tolist(),
            "y_train": y_train.tolist(),
            "y_test": y_test.tolist(),
            "random_state": random_state  # Output the used seed
        }
