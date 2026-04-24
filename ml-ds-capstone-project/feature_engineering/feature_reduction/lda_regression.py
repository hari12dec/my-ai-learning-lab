import pandas as pd

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
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
def split_scalar(indep_X, dep_Y):
    X_train, X_test, y_train, y_test = train_test_split(
        indep_X, dep_Y, test_size=0.25, random_state=0
    )

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    return X_train, X_test, y_train, y_test


# ---------------- COMMON METRICS ----------------
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


# ---------------- MAIN LDA + REGRESSION ----------------
def lda_regression_result(dataset, target):

    # Example: change target to continuous column
    indep_X = dataset.drop(target, axis=1)
    dep_Y = dataset[target]

    # Apply LDA (only if target is categorical → otherwise skip LDA)
    lda = LDA(n_components=2)
    X_lda = lda.fit_transform(indep_X, dataset[target])

    indep_X = pd.DataFrame(X_lda, columns=['LD1', 'LD2'])

    # Split
    X_train, X_test, y_train, y_test = split_scalar(indep_X, dep_Y)

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