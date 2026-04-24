import numpy as np
import pandas as pd
import pickle

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor


# ---------------- FEATURE ENGINEERING ----------------
class FeatureEngineer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()

        # 🔥 Required raw feature
        if "hour" not in df.columns:
            raise ValueError("hour column is required")

        # ---- Create features ----
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)

        df["dist_x_traffic"] = df["distance_km"] * df["Traffic"]
        df["distance_x_peak"] = df["distance_km"] * df["is_peak"]

        df["peak_weight"] = df["hour"].apply(
            lambda x: 2 if 18 <= x <= 21 else (1 if 12 <= x <= 14 else 0)
        )

        return df


# ---------------- FEATURE SELECTOR ----------------
class FeatureSelector(BaseEstimator, TransformerMixin):

    def __init__(self, features):
        self.features = features

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.features]


# ---------------- FINAL FEATURES ----------------
final_features = [
    'Agent_Age',
    'Agent_Rating',
    'Traffic',
    'distance_km',
    'hour_sin',
    'is_peak',
    'dist_x_traffic',
    'distance_x_peak',
    'peak_weight',
    'Weather_Sunny',
    'Area_Urban',
    'Category_Grocery'
]


# ---------------- BUILD PIPELINE ----------------
def build_pipeline():

    pipeline = Pipeline([
        ("feature_engineering", FeatureEngineer()),
        ("feature_selection", FeatureSelector(final_features)),
        ("model", RandomForestRegressor(
            n_estimators=300,
            max_depth=12,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=0,
            n_jobs=-1
        ))
    ])

    return pipeline


# ---------------- TRAIN + SAVE ----------------
def modelCreation(df, target, model_name):

    df = df.copy()

    # 🔥 Validate required raw columns
    required_cols = [
        'Agent_Age', 'Agent_Rating', 'Traffic',
        'distance_km', 'hour', 'is_peak',
        'Weather_Sunny', 'Area_Urban', 'Category_Grocery'
    ]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"{col} missing in dataset")

    X = df.drop(target, axis=1)
    y = df[target]

    pipeline = build_pipeline()

    pipeline.fit(X, y)

    with open(f"{model_name}.sav", "wb") as f:
        pickle.dump(pipeline, f)

    print(f"Model saved as {model_name}.sav")


# ---------------- PREDICTION ----------------
def modelPrediction(model_name, sampleData):

    df = sampleData.copy()

    # 🔥 Validate input
    required_cols = [
        'Agent_Age', 'Agent_Rating', 'Traffic',
        'distance_km', 'hour', 'is_peak',
        'Weather_Sunny', 'Area_Urban', 'Category_Grocery'
    ]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"{col} missing in input data")

    with open(f"{model_name}.sav", "rb") as f:
        model = pickle.load(f)

    prediction = model.predict(df)

    return float(prediction[0])