import numpy as np
from sklearn.metrics import r2_score

from AINodes.src.core.basic_node import BasicNode


class R2ScoreBasicNode(BasicNode):
    def __init__(self, node_id):
        """Berechnet den R²-Wert für ein trainiertes Modell."""
        super().__init__(node_id)

        # Inputs: Vorhergesagte Werte & tatsächliche Werte
        self.input_y_true = self.add_socket("input", "array", "y_true")
        self.input_y_pred = self.add_socket("input", "array", "y_pred")

        # Output: R²-Score
        self.output_score = self.add_socket("output", "float", "r2_score")

    def execute(self):
        """Berechnet den R²-Wert und gibt ihn aus."""
        y_true = self.input_y_true.pass_data()
        y_pred = self.input_y_pred.pass_data()

        if y_true is None or y_pred is None:
            print("Fehlende Eingaben für R2ScoreNode")
            return None

        # Konvertiere zu NumPy-Arrays
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        # Berechne den R²-Wert
        score = r2_score(y_true, y_pred)
        return {"r2_score": score}
