from typing import Literal

import pandas as pd
from pandas import DateOffset

from modelhub.core.preprocessor.preprocessor import Preprocessor


class RegressorPreprocessor(Preprocessor):
    """
    Regressor preprocessing
    """

    def __init__(self) -> None:
        pass

    def preprocess(
        self,
        df: pd.DataFrame,
        level: Literal["segment", "hour"] = "hour",
        shift: bool = True,
    ):
        """
        Preprocess the data before training
        :param df: Dataframe to preprocess
        :param level: Level to aggregate to
        :param shift: Whether to shift the data
        """
        df = df.copy()
        df = super().preprocess(df)

        df = df.groupby(["timestamp", "segment_id"]).mean().reset_index()
        df = df.groupby(["timestamp"]).mean().reset_index()
        df.drop(columns=["segment_id"], inplace=True)
        df.index = df["timestamp"]
        df.drop(columns=["timestamp"], inplace=True)
        aqi_cols = [col for col in df.columns if "_aqi" in col]
        cols_to_drop = [
            "v85",
            "latitude",
            "longitude",
            "altitude",
            "distance_km",
            "heavy",
            "car",
            "p1",
            "p2",
            *aqi_cols,
        ]
        df.drop(columns=cols_to_drop, inplace=True)
        if shift:
            if level == "segment":
                df["aqi"] = df.groupby("segment_id")["aqi"].shift(-1)
            else:
                df["aqi"] = df["aqi"].shift(-1)
        df.dropna(inplace=True)
        X_train, y_train, X_test, y_test = self.split_time_series(df, "aqi")
        return X_train, y_train, X_test, y_test

    def split_time_series(self, df, target, hard_split=False):
        if hard_split:
            # Hard split based on the date range
            split_point = df.index.max() - DateOffset(days=7, hour=12)
            train = df[df.index <= split_point]
            test = df[df.index > split_point]
        else:
            df_hourly = df.resample("H").ffill()
            train_size_hourly = int(len(df_hourly) * 0.8)
            train = df_hourly.iloc[:train_size_hourly]
            test = df_hourly.iloc[train_size_hourly:]

        y_train = train[target]
        X_train = train.drop(columns=[target])
        y_test = test[target]
        X_test = test.drop(columns=[target])
        return X_train, y_train, X_test, y_test

    def preprocess_prediction(self, df):
        """
        Preprocess the data before making predictions
        """
        df = df.copy()
        print("Preprocessing prediction data")
        df = super().preprocess(df)
        aqi_cols = [col for col in df.columns if "_aqi" in col]
        cols_to_drop = [
            "v85",
            "latitude",
            "segment_id",
            "aqi",
            "longitude",
            "altitude",
            "distance_km",
            "heavy",
            "car",
            "p1",
            "p2",
            *aqi_cols,
        ]
        df.drop(columns=cols_to_drop, inplace=True)
        print("Regression preprocessing complete")
        return df
