from sklearn.linear_model import LinearRegression

from AINodes.src.core.ml_node import MlNode


class LinearRegressionNode(MlNode):
    """
    A node that trains a linear regression model and generates predictions.

    Functionality:
    - Accepts training data (X_train, y_train) and test data (X_test) as input.
    - Uses Scikit-Learn's LinearRegression model for training.
    - Outputs the trained model and predicted values for X_test.

    Inputs:
    - `x_train` (array): Feature matrix for training (2D array).
    - `y_train` (array): Target values for training (1D array).
    - `x_test` (array): Feature matrix for making predictions (2D array).

    Outputs:
    - `model` (LinearRegression): The trained linear regression model.
    - `predictions` (array): Predicted values for X_test.
    """

    def __init__(self, node_type: str):
        """
        Initializes a linear regression node.

        :param node_type: A unique identifier for the node.
        """
        super().__init__(node_type)
        self.model = LinearRegression()  # Instance of the linear regression model

        # Define input sockets
        self.input_x_train = self.add_socket("input", "array", "x_train")  # Training features
        self.input_y_train = self.add_socket("input", "array", "y_train")  # Training targets
        self.input_x_test = self.add_socket("input", "array", "x_test")  # Test features

        # Define output sockets
        self.output_model = self.add_socket("output", "model", "model")  # Trained model
        self.output_predictions = self.add_socket("output", "array", "predictions")  # Model predictions

    def compute(self):
        """
        Executes the linear regression model.

        Workflow:
        1. Retrieve input data from connected nodes.
        2. Validate and reshape input arrays to ensure compatibility.
        3. Train a linear regression model on X_train and y_train.
        4. Generate predictions using X_test.
        5. Output the trained model and predictions.

        :return: Dictionary with keys:
                 - `"model"`: Trained LinearRegression model.
                 - `"predictions"`: List of predicted values.
        """
        X_train = self.input_x_train.pass_data()
        y_train = self.input_y_train.pass_data()
        X_test = self.input_x_test.pass_data()

        if X_train is None or y_train is None or X_test is None:
            print("⚠ Missing input data in LinearRegressionNode")
            return None

        # ✅ Automatically ensures correct shape!
        X_train, y_train = self.validate_X_y(X_train, y_train)
        X_test = self.validate_X(X_test)

        # Train the model
        self.model.fit(X_train, y_train)

        # Generate predictions
        predictions = self.model.predict(X_test)

        return {
            "model": self.model,
            "predictions": predictions.tolist()
        }

    def serialize_parameters(self)-> dict:
        return {}
