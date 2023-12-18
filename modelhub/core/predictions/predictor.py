import json
import os
import pickle
from datetime import date

import numpy as np
import pandas as pd
from sklearn.base import is_regressor

from modelhub.core.preprocessor.classifier_preprocessor import ClassifierPreprocessor
from modelhub.core.preprocessor.regressor_preprocessor import RegressorPreprocessor
from modelhub.services.blobstorage import BlobStorageAccessPoint


def pull_latest(func):
    """
    Decorator to check if there is a new model in the blob storage
    """

    def wrap(self, *args, **kwargs):
        """
        Check for the latest model, if current model is not the latest, pull it
        """
        if self.last_pulled != date.today():
            self.last_pulled = date.today()
            BlobStorageAccessPoint().pull_models()
            self.models = [
                pickle.load(open(os.path.join(os.getcwd(), "models", model), "rb"))
                for model in os.listdir(os.path.join(os.getcwd(), "models"))
            ]
            result = func(self, *args, **kwargs)
            return result
        else:
            return func(self, *args, **kwargs)

    return wrap


class Predictor:
    """
    Predict future values, recognize anomalies, aggregate everything into a json message
    to put on a queue
    """

    def __init__(self) -> None:
        self.last_pulled = None
        self.models = []
        self.regressor_preprocessor = RegressorPreprocessor()
        self.classifier_preprocessor = ClassifierPreprocessor()

    @pull_latest
    def predict_batch(self, aggregated_messages):
        """
        Predict values for a batch of messages
        """
        aggregated_messages = [json.loads(result) for result in aggregated_messages]
        aggregated_messages = pd.DataFrame(aggregated_messages)
        all_regressor_predictions = []
        all_classifier_predictions = []
        # Process each model
        for model in self.models:
            # Determine if the model is a regressor or classifier
            is_regressor_model = is_regressor(model)

            # Preprocess messages based on model type
            if is_regressor_model:
                preprocessed_messages = (
                    self.regressor_preprocessor.preprocess_prediction(
                        aggregated_messages,
                    )
                )
            else:
                preprocessed_messages = (
                    self.classifier_preprocessor.preprocess_prediction(
                        aggregated_messages,
                    )
                )
            # Predict using the model and store predictions
            model_predictions = model.predict(preprocessed_messages)
            print(model_predictions)
            if is_regressor_model:
                all_regressor_predictions.append(model_predictions)
            else:
                all_classifier_predictions.append(model_predictions)
        avg_regressor_predictions = (
            np.mean(all_regressor_predictions, axis=0)
            if all_regressor_predictions
            else np.zeros(len(aggregated_messages))
        )

        avg_classifier_predictions = (
            np.mean(all_classifier_predictions, axis=0)
            if all_classifier_predictions
            else np.zeros(len(aggregated_messages))
        )

        avg_classifier_predictions = np.where(
            avg_classifier_predictions > 0,
            False,
            True,
        )
        return {
            "regressor": avg_regressor_predictions,
            "classifier": avg_classifier_predictions,
        }
