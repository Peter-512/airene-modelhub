from sklearn.ensemble import IsolationForest

from modelhub.core.predictions.ai_models.model import Model
from modelhub.core.preprocessor.prediction_preprocessor import PredictionPreprocessor


class IsolationForestModel(Model):
    def __init__(self, preprocessor=PredictionPreprocessor()):
        self.model = IsolationForest()
        self.preprocessor = preprocessor

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X):
        return self.model.predict(X)
