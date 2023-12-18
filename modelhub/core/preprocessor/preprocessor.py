import logging
from abc import ABC, abstractmethod

import pandas as pd


class Preprocessor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def preprocess(self, df) -> pd.DataFrame:
        """
        Base preprocess method

        :param df: The dataframe to preprocess
        :return: The preprocessed dataframe
        """
        logging.info("Preprocessing data")
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.index = df["timestamp"]
        df.drop(
            columns=[
                "id",
                "coordinates",
                "timestamp",
                "sensor_type",
                "current.last_updated",
                "current.air_quality.us-epa-index",
                "current.air_quality.gb-defra-index",
            ],
            inplace=True,
        )
        # drop azure columns if they exist
        try:
            azure_cols = ["_rid", "_self", "_etag", "_attachments", "_ts"]
            df.drop(columns=azure_cols, inplace=True)
        except Exception:
            pass

        # Convert all columns except 'timestamp' to float
        for col in df.columns:
            try:
                df[col] = df[col].astype(float)
            except Exception:
                df.drop(columns=[col], inplace=True)
        # Convert all columns except 'timestamp' to float
        df.dropna(inplace=True)
        df["total_traffic"] = df["heavy"] + df["car"]
        df["dayofweek"] = df.index.dayofweek
        df["hour"] = df.index.hour
        df = self.add_air_quality_indices(df)
        aqi_cols = [col for col in df.columns if "_aqi" in col]
        df["aqi"] = df[aqi_cols].mean(axis=1)
        return df

    @abstractmethod
    def preprocess_prediction(self, df) -> pd.DataFrame:
        pass

    def add_air_quality_indices(self, local_df):
        """
        Add air quality indices to the dataframe

        :param local_df: The dataframe to add the indices to

        :return: The dataframe with the indices added
        """

        # European Air Quality Standards
        standards = pd.DataFrame(
            [[20, 125, 40, 40, 10000, 120]],
            columns=["pm25", "so2", "no2", "pm10", "co", "o3"],
        )

        column_mappings = {
            "co": "current.air_quality.co",
            "no2": "current.air_quality.no2",
            "o3": "current.air_quality.o3",
            "so2": "current.air_quality.so2",
            "pm25": "current.air_quality.pm2_5",
            "pm10": "current.air_quality.pm10",
        }

        def aqi_(column_name: str):
            mapped_name = column_mappings.get(column_name)
            return local_df[mapped_name] / standards[column_name].values[0] * 100

        for column in column_mappings.keys():
            local_df[f"{column}_aqi"] = aqi_(column)

        aqi_columns = [f"{column}_aqi" for column in column_mappings.keys()]
        is_series = type(local_df) == pd.Series

        # Iterate each row if it is a dataframe, else iterate each column if it is a series (single row)
        local_df["aqi"] = local_df[aqi_columns].mean(axis=1 if not is_series else 0)
        return local_df
