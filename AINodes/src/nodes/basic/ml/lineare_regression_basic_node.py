from typing import Optional, Dict, Any

import numpy as np
from sklearn.linear_model import LinearRegression

from AINodes.src.core.basic_node import BasicNode


class LinearRegressionNode(BasicNode):
    """
    A node that trains a linear regression model and generates predictions.
    - Takes training data (X_train, y_train) and test data (X_test) as input.
    - Outputs the trained model and predicted values.
    """

    def __init__(self, node_id: str):
        """
        Initializes a linear regression node.

        :param node_id: A unique identifier for the node.
        """
        super().__init__(node_id)
        self.model = LinearRegression()  # Instance of the linear regression model

        # Define input sockets
        self.input_x_train = self.add_socket("input", "array", "x_train")  # Training features
        self.input_y_train = self.add_socket("input", "array", "y_train")  # Training targets
        self.input_x_test = self.add_socket("input", "array", "x_test")  # Test features

        # Define output sockets
        self.output_model = self.add_socket("output", "model", "model")  # Trained model
        self.output_predictions = self.add_socket("output", "array", "predictions")  # Model predictions

    def compute(self) -> Optional[Dict[str, Any]]:
        """
        Trains a linear regression model using the provided training data and generates predictions.

        :return: A dictionary containing:
                 - "model": The trained LinearRegression instance.
                 - "predictions": A list of predicted values for X_test.
                 Returns None if any input data is missing.
        """
        X_train = self.input_x_train.pass_data()
        y_train = self.input_y_train.pass_data()
        X_test = self.input_x_test.pass_data()

        if X_train is None or y_train is None or X_test is None:
            print("Error: Missing input data in LinearRegressionNode.")
            return None

        # Convert inputs to NumPy arrays and reshape X_train & X_test for sklearn
        X_train = np.array(X_train).reshape(-1, 1)
        y_train = np.array(y_train)
        X_test = np.array(X_test).reshape(-1, 1)

        # Train the linear regression model
        self.model.fit(X_train, y_train)

        # Generate predictions
        predictions = self.model.predict(X_test)

        return {
            "model": self.model,  # Trained model instance
            "predictions": predictions.tolist()  # Convert predictions to a Python list
        }
