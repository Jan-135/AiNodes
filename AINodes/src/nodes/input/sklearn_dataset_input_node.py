from typing import Optional, Dict, List, Union

from sklearn import datasets

from AINodes.src.core.input_node import InputNode


class SklearnDatasetInputNode(InputNode):
    """
    A node that loads predefined datasets from sklearn.
    - Outputs the dataset in three different formats:
      1️⃣ The full dataset as a dictionary: {"features": X, "targets": y}
      2️⃣ Only the feature matrix (X)
      3️⃣ Only the target labels (y)
    """

    AVAILABLE_DATASETS = {
        "iris": datasets.load_iris,
        "wine": datasets.load_wine,
        "california_housing": datasets.fetch_california_housing,
    }

    def __init__(self, node_type: str, dataset_name: str = "iris"):
        """
        Initializes the dataset input node.

        :param node_type: A unique identifier for the node.
        :param dataset_name: The name of the dataset to load.
        """
        super().__init__(node_type)
        self.dataset_name: str = dataset_name  # Selected dataset name

        # Define output sockets
        self.output_dict = self.add_socket("output", "dict", "dataset_dict")  # Full dataset as dictionary
        self.output_X = self.add_socket("output", "array", "features")  # Feature matrix (X)
        self.output_y = self.add_socket("output", "array", "targets")  # Target labels (y)

    def compute(self) -> Optional[Dict[str, Union[Dict[str, List[Union[float, int]]], List[List[float]], List[int]]]]:
        """
        Loads the selected dataset and returns its features (X), targets (y), and full dataset dictionary.

        :return: A dictionary containing:
                 - "dataset_dict": A dictionary with {"features": X, "targets": y}
                 - "features": The feature matrix (X) as a list of lists
                 - "targets": The target labels (y) as a list
                 Returns None if the dataset is invalid or cannot be loaded.
        """
        if self.dataset_name not in self.AVAILABLE_DATASETS:
            print(f"Error: Dataset '{self.dataset_name}' is not supported.")
            return None

        try:
            # Load dataset
            dataset = self.AVAILABLE_DATASETS[self.dataset_name]()

            # Convert NumPy arrays to Python lists
            X: List[List[float]] = dataset.data.tolist()
            y: List[Union[int, float]] = dataset.target.tolist()

            return {
                "dataset_dict": {"features": X, "targets": y},  # Full dataset dictionary
                "features": X,  # Features only
                "targets": y  # Labels only
            }

        except Exception as e:
            print(f"Error loading dataset '{self.dataset_name}': {e}")
            return None
