import pandas as pd
import numpy as np
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor


def modelCreation(df, selected_features, target, model_name):

    # 🔥 Feature Engineering
    df["peak_x_traffic"] = df["is_peak"] * df["Traffic"]
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)

    # 🔥 Validation
    for col in selected_features:
        if col not in df.columns:
            raise ValueError(f"{col} not found in dataset")

    X = df[selected_features]
    y = df[target]

    # 🔥 Pipeline
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", GradientBoostingRegressor(
            n_estimators=300,
            learning_rate=0.03,
            max_depth=5,
            random_state=0
        ))
    ])

    # Train
    pipeline.fit(X, y)

    # Save
    joblib.dump(pipeline, f"{model_name}.pkl")

    print(f"Model saved as {model_name}.pkl")

def modelPrediction(model_name, sampleData):
    # Load model
    loaded_model = joblib.load(f"{model_name}.pkl")
    prediction = loaded_model.predict(sampleData)
    return prediction[0]


