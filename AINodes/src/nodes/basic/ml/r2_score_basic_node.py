from typing import Optional, Dict, Any

import numpy as np
from sklearn.metrics import r2_score

from AINodes.src.core.basic_node import BasicNode


class R2ScoreBasicNode(BasicNode):
    """
    A node that calculates the R² score for a trained model.
    - Compares predicted values with actual values to evaluate model performance.
    """

    def __init__(self, node_id: str):
        """
        Initializes an R² score node.

        :param node_id: A unique identifier for the node.
        """
        super().__init__(node_id)

        # Inputs: True values & predicted values
        self.input_y_true = self.add_socket("input", "array", "y_true")
        self.input_y_pred = self.add_socket("input", "array", "y_pred")

        # Output: R² score
        self.output_score = self.add_socket("output", "float", "r2_score")

    def compute(self) -> Optional[Dict[str, Any]]:
        """
        Computes the R² score based on the provided true and predicted values.

        :return: A dictionary containing the R² score, or None if inputs are missing.
        """
        y_true = self.input_y_true.pass_data()
        y_pred = self.input_y_pred.pass_data()

        if y_true is None or y_pred is None:
            print("Missing inputs for R2ScoreBasicNode")
            return None

        # Convert to NumPy arrays
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        # Compute the R² score
        score = r2_score(y_true, y_pred)
        return {"r2_score": score}
