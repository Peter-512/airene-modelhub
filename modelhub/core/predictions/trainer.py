from typing import List

from modelhub.core.predictions.ai_models.model import Model
from modelhub.services.cosmosdb import CosmosDBAccessPoint


class Trainer:
    def __init__(self, models: List[Model], debug_data=None) -> None:
        self.models = models
        self.db = CosmosDBAccessPoint() if debug_data is None else None
        self.debug_data = debug_data

    def train(self):
        if self.debug_data is None:
            df = self.retrieve_data()
        else:
            df = self.debug_data

        for model in self.models:
            X_train, y_train, X_test, y_test = model.preprocessor.preprocess(df)
            model.fit(X_train, y_train, X_test, y_test)
            # model.evaluate(X_test, y_test)
            model.save()

    def retrieve_data(self):
        return self.db.query_all()
