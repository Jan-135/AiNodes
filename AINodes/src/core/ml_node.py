from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple, Any

from AINodes.src.core.basic_node import BasicNode


class MlNode(BasicNode, ABC):
    """
    Abstract base class for all machine learning nodes.
    - Ensures `X` is always 2D and `y` is always 1D.
    - Provides a common interface for ML-related nodes.
    """

    def __init__(self, node_id: str):
        """
        Initializes a machine learning node.

        :param node_id: Unique identifier for the node.
        """
        super().__init__(node_id)

    @abstractmethod
    def compute(self) -> Any:
        """
        Abstract method that must be implemented by subclasses.
        Defines how the ML node processes data.
        """
        pass

    def validate_X_y(self, X: Any, y: Any) -> Tuple[np.ndarray, np.ndarray]:
        """
        Validates and reshapes input data:
        - Ensures `X` is always a 2D array of shape (n_samples, n_features).
        - Ensures `y` is always a 1D array of shape (n_samples,).

        :param X: Feature matrix (list, NumPy array, or similar).
        :param y: Target vector (list, NumPy array, or similar).
        :return: Tuple (X, y) in the correct shape.
        :raises ValueError: If X or y is empty or invalid.
        """
        X = np.array(X, dtype=np.float64)  # Convert to NumPy array (force float for ML)
        y = np.array(y, dtype=np.float64)  # Convert to NumPy array (force float for ML)

        if X.size == 0 or y.size == 0:
            raise ValueError("X and y cannot be empty.")

        # Ensure X is 2D
        if X.ndim == 1:
            X = X.reshape(-1, 1)  # Convert (n,) to (n,1)

        # Ensure y is 1D
        y = y.ravel()  # Convert (n,1) to (n,)

        return X, y

    def validate_X(self, X: Any) -> np.ndarray:
        """
        Ensures `X` is always a 2D array (useful for nodes that only process features).

        :param X: Feature matrix (list, NumPy array, or similar).
        :return: X in the correct shape.
        :raises ValueError: If X is empty or invalid.
        """
        X = np.array(X, dtype=np.float64)

        if X.size == 0:
            raise ValueError("X cannot be empty.")

        # Ensure X is 2D
        if X.ndim == 1:
            X = X.reshape(-1, 1)

        return X
