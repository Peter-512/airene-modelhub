import pandas as pd
from sklearn.model_selection import train_test_split

from modelhub.core.preprocessor.preprocessor import Preprocessor


class ClassifierPreprocessor(Preprocessor):
    def __init__(self):
        pass

    def preprocess(self, df):
        """
        Preprocess the data before training

        :param df: The dataframe to preprocess
        :return: The preprocessed dataframe
        """
        local_df = df.copy()
        local_df = super().preprocess(local_df)
        y = local_df["aqi"]
        X = local_df.drop(["aqi"], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        return X_train, y_train, X_test, y_test

    def preprocess_prediction(self, df) -> pd.DataFrame:
        """
        Preprocess the data before making predictions

        :param df: The dataframe to preprocess
        :return: The preprocessed dataframe
        """
        local_df = df.copy()
        local_df = super().preprocess(local_df)
        return local_df
