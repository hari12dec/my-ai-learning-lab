import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR


def split_scale(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train, X_test, y_train, y_test


def r2(model, X_test, y_test):
    return r2_score(y_test, model.predict(X_test))


def run_models(X_train, y_train, X_test, y_test):
    results = {}

    models = {
        "Linear": LinearRegression(),
        "SVM": SVR(kernel="rbf"),
        "Decision": DecisionTreeRegressor(random_state=0),
        "Random": RandomForestRegressor(n_estimators=100, random_state=0),
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
        results[name] = r2(model, X_test, y_test)

    return results


def rfe_regression_result(dataset, target, n_features=10):

    # Encode if needed
    if dataset.select_dtypes(include="object").shape[1] > 0:
        df = pd.get_dummies(dataset, drop_first=True)
    else:
        df = dataset.copy()

    # Handle NaN
    df = df.fillna(df.median(numeric_only=True))

    X = df.drop(target, axis=1)
    y = df[target]

    # RFE (use Linear model)
    model = LinearRegression()
    selector = RFE(
    estimator=LinearRegression(),
    n_features_to_select=n_features,
    step=2  
    )
    selector.fit(X, y)

    selected_cols = X.columns[selector.support_]
    print("Selected Features:", list(selected_cols))

    X_selected = X[selected_cols]

    # Split + scale
    X_train, X_test, y_train, y_test = split_scale(X_selected, y)

    # Run models
    results = run_models(X_train, y_train, X_test, y_test)

    result_df = pd.DataFrame([results], index=["RFE"])

    return result_df