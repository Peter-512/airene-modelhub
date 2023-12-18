import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from modelhub.core.predictions.ai_models._isolation_forest import IsolationForestModel
from modelhub.core.predictions.ai_models.model import Model
from modelhub.core.preprocessor.classifier_preprocessor import ClassifierPreprocessor


class XGBoostClassifierModel(Model):
    def __init__(self, preprocessor=ClassifierPreprocessor()):
        super().__init__()
        self.model = XGBClassifier()
        self.helper_model = IsolationForestModel()
        self.preprocessor = preprocessor

    def fit(self, X_train, y_train, X_test, y_test):
        """
        Train the model
        """
        # Recombine X_train and y_train with X_test and y_test
        # so we can train the helper model
        X_combined = pd.concat([X_train, X_test], axis=0)
        y_combined = pd.concat([y_train, y_test], axis=0)
        X_combined = pd.concat([X_combined, y_combined], axis=1)

        # Ensure the columns are of string type
        X_combined.columns = X_combined.columns.astype(str)

        # Drop any rows with missing values
        X_combined.dropna(inplace=True)
        X_combined.reset_index(inplace=True)

        # Generate new labels using the helper model
        augmented_df = self.helper_model.create_labels(X_combined)

        # Split the augmented dataframe into training and testing sets
        (X_train, X_test, y_train, y_test) = train_test_split(
            augmented_df.drop(["anomaly"], axis=1),
            augmented_df["anomaly"],
            test_size=0.2,
            random_state=42,
        )
        # def objective(trial):
        #     param = {
        #         "verbosity": 0,
        #         "objective": "binary:logistic",
        #         "booster": trial.suggest_categorical(
        #             "booster", ["gbtree", "gblinear", "dart"]
        #         ),
        #         "lambda": trial.suggest_loguniform("lambda", 1e-8, 1.0),
        #         "alpha": trial.suggest_loguniform("alpha", 1e-8, 1.0),
        #     }
        #     if param["booster"] == "gbtree" or param["booster"] == "dart":
        #         param["max_depth"] = trial.suggest_int("max_depth", 1, 9)
        #         param["eta"] = trial.suggest_loguniform("eta", 1e-8, 1.0)
        #         param["gamma"] = trial.suggest_loguniform("gamma", 1e-8, 1.0)
        #         param["grow_policy"] = trial.suggest_categorical(
        #             "grow_policy", ["depthwise", "lossguide"]
        #         )

        #     clf = XGBClassifier(**param)
        #     clf.fit(X_train, y_train)
        #     return clf.score(X_train, y_train)

        # study = optuna.create_study(direction="maximize")
        # study.optimize(objective, n_trials=100)

        # self.model = XGBClassifier(**study.best_params)
        self.model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
