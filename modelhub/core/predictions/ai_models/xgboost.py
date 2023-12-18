from xgboost import XGBRegressor

from modelhub.core.predictions.ai_models.model import Model
from modelhub.core.preprocessor.regressor_preprocessor import RegressorPreprocessor


class XGBoostRegressorModel(Model):
    """
    XGBoost Regressor model
    """

    def __init__(self, preprocessor=RegressorPreprocessor()):
        super().__init__()
        self.model = XGBRegressor()
        self.preprocessor = preprocessor

    def fit(self, X_train, y_train, X_test, y_test):
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

        #     clf = XGBRegressor(**param)
        #     clf.fit(X_train, y_train)
        #     return clf.score(X_train, y_train)

        # study = optuna.create_study(direction="maximize")
        # study.optimize(objective, n_trials=100)

        # self.model = XGBRegressor(**study.best_params)
        self.model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
