from sklearn.ensemble import IsolationForest

from modelhub.core.predictions.ai_models.model import Model
from modelhub.core.preprocessor.regressor_preprocessor import RegressorPreprocessor


class IsolationForestModel(Model):
    """
    Helper model to label data, so then we can deploy a supervised model for
    anomaly detection
    """

    def __init__(self, preprocessor=RegressorPreprocessor()):
        self.model = IsolationForest(
            n_estimators=1000,
            max_samples=2048,
            contamination="auto",
        )
        self.preprocessor = preprocessor

    def fit(self, X_train, y_train, X_test, y_test):
        self.model.fit(X_train, y_train, X_test, y_test)

    def create_labels(self, X):
        """
        Create labels for the data, so we can train a supervised model
        """
        X.drop(columns=["timestamp"], inplace=True)
        self.model.fit(X)
        predictions = self.model.predict(X)
        X["anomaly"] = predictions
        X["anomaly"] = X["anomaly"].map({1: 0, -1: 1})
        return X
