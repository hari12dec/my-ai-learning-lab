import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ---------------- REGRESSION MODELS ----------------
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

# ---------------- METRICS ----------------
from sklearn.metrics import mean_squared_error, r2_score


# ---------------- SPLIT + SCALING ----------------
def split_scale(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    return X_train, X_test, y_train, y_test


# ---------------- METRICS ----------------
def reg_metrics(model, X_test, y_test):
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    return mse, rmse, r2


# ---------------- MODELS ----------------
def linear_reg(X_train, y_train, X_test, y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return reg_metrics(model, X_test, y_test)


def svm_reg(X_train, y_train, X_test, y_test):
    model = SVR(kernel='rbf')
    model.fit(X_train, y_train)
    return reg_metrics(model, X_test, y_test)


def knn_reg(X_train, y_train, X_test, y_test):
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    return reg_metrics(model, X_test, y_test)


def decision_tree_reg(X_train, y_train, X_test, y_test):
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    return reg_metrics(model, X_test, y_test)


def random_forest_reg(X_train, y_train, X_test, y_test):
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    return reg_metrics(model, X_test, y_test)


# ---------------- MAIN PCA + REGRESSION ----------------
def pca_regression_result(dataset, target, n_components=5):

    # Encode if needed
    if dataset.select_dtypes(include="object").shape[1] > 0:
        df = pd.get_dummies(dataset, drop_first=True)
    else:
        df = dataset.copy()

    # Handle NaN
    df = df.fillna(df.median(numeric_only=True))

    # Split features and target
    X = df.drop(target, axis=1)
    y = df[target]

    # Split first (important for no leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )

    # Scaling (MANDATORY for PCA)
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Apply PCA
    pca = PCA(n_components=n_components)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    print("Explained Variance Ratio:", pca.explained_variance_ratio_)
    print("Total Variance Covered:", sum(pca.explained_variance_ratio_))

    # Run models
    results = {}

    results['Linear Regression'] = linear_reg(X_train, y_train, X_test, y_test)
    results['SVM'] = svm_reg(X_train, y_train, X_test, y_test)
    results['KNN'] = knn_reg(X_train, y_train, X_test, y_test)
    results['Decision Tree'] = decision_tree_reg(X_train, y_train, X_test, y_test)
    results['Random Forest'] = random_forest_reg(X_train, y_train, X_test, y_test)

    # Convert to DataFrame
    result_df = pd.DataFrame(
        [(k, v[0], v[1], v[2]) for k, v in results.items()],
        columns=['Model', 'MSE', 'RMSE', 'R2 Score']
    )

    print(result_df)
    return result_df