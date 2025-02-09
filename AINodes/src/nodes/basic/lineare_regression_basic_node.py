import numpy as np
from sklearn.linear_model import LinearRegression

from AINodes.src.core.basic_node import BasicNode


class LinearRegressionNode(BasicNode):
    def __init__(self, node_id):
        """Trainiert eine lineare Regression und gibt Modell & Vorhersagen zurück."""
        super().__init__(node_id)
        self.model = LinearRegression()

        # Inputs: Trainingsdaten X, Zielwerte y, Testdaten X_test
        self.input_x_train = self.add_socket("input", "array", "x_train")
        self.input_y_train = self.add_socket("input", "array", "y_train")
        self.input_x_test = self.add_socket("input", "array", "x_test")

        # Outputs: Trainiertes Modell & Vorhersagen
        self.output_model = self.add_socket("output", "model", "model")
        self.output_predictions = self.add_socket("output", "array", "predictions")

    def compute(self):
        """Trainiert eine lineare Regression und gibt das Modell & Vorhersagen zurück."""
        X_train = self.input_x_train.pass_data()
        y_train = self.input_y_train.pass_data()
        X_test = self.input_x_test.pass_data()

        if X_train is None or y_train is None or X_test is None:
            print("Fehlende Eingabedaten in LinearRegressionNode")
            return None

        X_train = np.array(X_train).reshape(-1, 1)
        y_train = np.array(y_train)
        X_test = np.array(X_test).reshape(-1, 1)

        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)

        print("hallo")

        return {
            "model": self.model,
            "predictions": predictions.tolist()
        }
