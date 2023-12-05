import os
import pickle
from abc import ABC, abstractmethod
from datetime import date

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from modelhub.services.blobstorage import BlobStorageAccessPoint


class Model(ABC):
    def __init__(self, model_path="/tmp"):
        # Create models_date folder in tmp
        self.model_path = os.path.join(
            model_path,
            "models",
        )
        self.model = None
        self.preprocessor = None
        self.blobap = BlobStorageAccessPoint()
        os.makedirs(self.model_path, exist_ok=True)

    @abstractmethod
    def train(self, X_train, y_train, X_test, y_test):
        print(f"Training {self.__class__.__name__}")

    @abstractmethod
    def predict(self, X):
        pass

    def save(self):
        print("Saving model")
        file_name = os.path.join(
            self.model_path,
            f"{self.__class__.__name__}_{date.today()}.pkl",
        )
        pickle.dump(self.model, open(file_name, "wb"))
        self.blobap.upload_blob(file_name)
        print("Model saved at ", file_name)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model and save evaluation results.
        """
        y_pred = self.predict(X_test)

        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        # Save metrics to a log file
        log_file = os.path.join(self.model_path, "evaluation_log.txt")
        with open(log_file, "w") as f:
            f.write(f"Mean Absolute Error (MAE): {mae}\n")
            f.write(f"Mean Squared Error (MSE): {mse}\n")
            f.write(f"Root Mean Squared Error (RMSE): {rmse}\n")
            f.write(f"R2 Score: {r2}\n")

        # Optionally print metrics
        print(f"Evaluation metrics saved to {log_file}")
