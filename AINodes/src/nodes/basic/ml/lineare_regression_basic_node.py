from sklearn.linear_model import LinearRegression

from AINodes.src.core.ml_node import MlNode


class LinearRegressionNode(MlNode):
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

    def compute(self):
        X_train = self.input_x_train.pass_data()
        y_train = self.input_y_train.pass_data()
        X_test = self.input_x_test.pass_data()

        if X_train is None or y_train is None or X_test is None:
            print("Missing input data in LinearRegressionNode")
            return None

        # ✅ Automatically ensures correct shape!
        X_train, y_train = self.validate_X_y(X_train, y_train)
        X_test = self.validate_X(X_test)

        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)

        return {
            "model": self.model,
            "predictions": predictions.tolist()
        }
