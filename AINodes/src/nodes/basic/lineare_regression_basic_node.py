from AINodes.src.core.basic_node import BasicNode
from AINodes.src.sockets.Input_socket import InputSocket
from AINodes.src.sockets.output_socket import OutputSocket
from sklearn.linear_model import LinearRegression
import numpy as np


class LinearRegressionNode(BasicNode):
    def __init__(self, node_id):
        super().__init__(node_id)
        self.model = LinearRegression()

        # Inputs: Trainingsdaten X, Zielwerte y, Testdaten X_test
        self.input_x_train = InputSocket(self, "array")
        self.input_y_train = InputSocket(self, "array")
        self.input_x_test = InputSocket(self, "array")
        self.inputs.extend([self.input_x_train, self.input_y_train, self.input_x_test])

        # Outputs: Trainiertes Modell & Vorhersagen
        self.output_model = OutputSocket(self, "model", "model")
        self.output_predictions = OutputSocket(self, "array", "predictions")
        self.outputs.extend([self.output_model, self.output_predictions])

    def execute(self):
        """Trainiert eine lineare Regression und gibt das Modell & Vorhersagen zurück."""
        X_train = self.input_x_train.pass_data()
        y_train = self.input_y_train.pass_data()
        X_test = self.input_x_test.pass_data()

        if X_train is None or y_train is None or X_test is None:
            print("Fehlende Eingabedaten in LinearRegressionNode")
            return None

        # Konvertiere Eingaben zu NumPy-Arrays
        X_train = np.array(X_train).reshape(-1, 1)
        y_train = np.array(y_train)
        X_test = np.array(X_test).reshape(-1, 1)

        # Modell trainieren
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)

        return {
            "model": self.model,
            "predictions": predictions.tolist()  # Als Liste für bessere JSON-Kompatibilität
        }
