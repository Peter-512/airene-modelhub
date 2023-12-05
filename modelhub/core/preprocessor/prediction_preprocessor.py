import pandas as pd
from sklearn.decomposition import PCA

# Import split from sklearn
from sklearn.model_selection import train_test_split


class PredictionPreprocessor:
    def __init__(self) -> None:
        pass

    def preprocess(self, df: pd.DataFrame) -> None:
        # Drop columns that are not needed
        df = df.drop(
            columns=[
                "id",
                "_rid",
                "_self",
                "_etag",
                "_attachments",
                "_ts",
                "current.air_quality.us-epa-index",
                "current.air_quality.gb-defra-index",
            ],
        )
        df = self.pca_air_traffic(df)

        X_train, X_test, y_train, y_test = self.split(df)
        return X_train, X_test, y_train, y_test

    def pca_air_traffic(self, df):
        air_columns = [
            "current.air_quality.co",
            "current.air_quality.no2",
            "current.air_quality.o3",
            "current.air_quality.so2",
            "current.air_quality.pm2_5",
            "current.air_quality.pm10",
            "p1",
            "p2",
        ]
        traffic_collumns = ["heavy", "car"]

        traffic_df = df[traffic_collumns]
        air_df = df[air_columns]

        # 95% of the variance, this is done to retain as much information as possible
        pca = PCA(n_components=0.95)

        air_df.fillna(0, inplace=True)
        air_df_reduced = pca.fit_transform(air_df)

        traffic_df.fillna(0, inplace=True)
        traffic_df_reduced = pca.fit_transform(traffic_df)
        df["X"] = traffic_df_reduced[:, 0]
        df["y"] = air_df_reduced[:, 0]

        # We need to shift the y to predict the future
        df["y"] = df.groupby("segment_id")["y"].shift(-1)
        # Drop the nulls
        df.dropna(inplace=True)

        print(df.columns)
        return df

    def split(self, df):
        traffic_columns = ["heavy", "car", "segment_id"]
        X = df[traffic_columns]
        y = df["y"]
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
        )
        print(
            f"SHAPES: {X_train.shape}, {X_test.shape}, {y_train.shape}, {y_test.shape}",
        )
        return X_train, X_test, y_train, y_test
