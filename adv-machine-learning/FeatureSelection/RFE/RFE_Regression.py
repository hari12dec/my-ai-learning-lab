import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.metrics import r2_score

# ---------------- SPLIT + SCALE ----------------
def split_scalar(indep_X, dep_Y):
    X_train, X_test, y_train, y_test = train_test_split(
        indep_X, dep_Y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    return X_train, X_test, y_train, y_test


# ---------------- METRIC ----------------
def r2_prediction(regressor, X_test, y_test):
    y_pred = regressor.predict(X_test)
    return r2_score(y_test, y_pred)


# ---------------- MODELS ----------------
def Linear(X_train, y_train, X_test, y_test):
    from sklearn.linear_model import LinearRegression

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)


def svm_linear(X_train, y_train, X_test, y_test):
    from sklearn.svm import SVR

    regressor = SVR(kernel="linear")
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)


def svm_NL(X_train, y_train, X_test, y_test):
    from sklearn.svm import SVR

    regressor = SVR(kernel="rbf")
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)


def Decision(X_train, y_train, X_test, y_test):
    from sklearn.tree import DecisionTreeRegressor

    regressor = DecisionTreeRegressor(random_state=0)
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)


def random(X_train, y_train, X_test, y_test):
    from sklearn.ensemble import RandomForestRegressor

    regressor = RandomForestRegressor(n_estimators=10, random_state=0)
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)


# ---------------- RFE ----------------
def rfeFeature(indep_X, dep_Y, n):
    from sklearn.linear_model import LinearRegression
    from sklearn.svm import SVR
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor

    rfelist = []

    models = [
        LinearRegression(),
        SVR(kernel="linear"),
        DecisionTreeRegressor(random_state=0),
        RandomForestRegressor(n_estimators=10, random_state=0),
    ]

    for model in models:
        print(model)

        selector = RFE(estimator=model, n_features_to_select=n)
        selector.fit(indep_X, dep_Y)

        selected_features = selector.transform(indep_X)
        rfelist.append(selected_features)

    return rfelist


# ---------------- RESULT TABLE ----------------
def rfe_regression(acclin, accsvml, accdes, accrf):
    rfedataframe = pd.DataFrame(
        index=["Linear", "SVM", "DecisionTree", "RandomForest"],
        columns=["Linear", "SVM", "Decision", "Random"],
    )

    for i, idx in enumerate(rfedataframe.index):
        rfedataframe.loc[idx, "Linear"] = acclin[i]
        rfedataframe.loc[idx, "SVM"] = accsvml[i]
        rfedataframe.loc[idx, "Decision"] = accdes[i]
        rfedataframe.loc[idx, "Random"] = accrf[i]

    return rfedataframe


# ---------------- MAIN ----------------
def rfe_regression_result():
    dataset1 = pd.read_csv("prep.csv")

    df2 = pd.get_dummies(dataset1, drop_first=True)

    indep_X = df2.drop("classification_yes", axis=1)
    dep_Y = df2["classification_yes"]

    rfelist = rfeFeature(indep_X, dep_Y, 3)

    acclin, accsvml, accsvmnl, accdes, accrf = [], [], [], [], []

    for i in rfelist:
        X_train, X_test, y_train, y_test = split_scalar(i, dep_Y)

        acclin.append(Linear(X_train, y_train, X_test, y_test))
        accsvml.append(svm_linear(X_train, y_train, X_test, y_test))
        accsvmnl.append(svm_NL(X_train, y_train, X_test, y_test))
        accdes.append(Decision(X_train, y_train, X_test, y_test))
        accrf.append(random(X_train, y_train, X_test, y_test))

    result = rfe_regression(acclin, accsvml, accdes, accrf)

    print(result)
    return result