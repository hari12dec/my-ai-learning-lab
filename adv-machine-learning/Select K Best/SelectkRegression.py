import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, chi2

# Feature Selection
def selectkbest(indep_X, dep_Y, n):
    test = SelectKBest(score_func=chi2, k=n)
    fit1 = test.fit(indep_X, dep_Y)
    return fit1.transform(indep_X)

# Train Test Split
def split_scalar(indep_X, dep_Y):
    X_train, X_test, y_train, y_test = train_test_split(
        indep_X, dep_Y, test_size=0.25, random_state=0
    )
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train, X_test, y_train, y_test

# R2 Evaluation
def r2_prediction(regressor, X_test, y_test):
    from sklearn.metrics import r2_score
    y_pred = regressor.predict(X_test)
    return r2_score(y_test, y_pred)

def Linear(X_train, y_train, X_test, y_test):
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)

def svm_linear(X_train, y_train, X_test, y_test):
    from sklearn.svm import SVR
    regressor = SVR(kernel='linear')
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)

def svm_NL(X_train, y_train, X_test, y_test):
    from sklearn.svm import SVR
    regressor = SVR(kernel='rbf')
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)

def decision_tree(X_train, y_train, X_test, y_test):
    from sklearn.tree import DecisionTreeRegressor
    regressor = DecisionTreeRegressor(random_state=0)
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)

def random_forest(X_train, y_train, X_test, y_test):
    from sklearn.ensemble import RandomForestRegressor
    regressor = RandomForestRegressor(n_estimators=10, random_state=0)
    regressor.fit(X_train, y_train)
    return r2_prediction(regressor, X_test, y_test)

# Result Table
def selectk_regression(acclin, accsvml, accsvmnl, accdes, accrf):
    dataframe = pd.DataFrame(
        index=['ChiSquare'],
        columns=['Linear', 'SVMl', 'SVMnl', 'Decision', 'Random']
    )

    for number, index in enumerate(dataframe.index):
        dataframe.loc[index, 'Linear'] = acclin[number]
        dataframe.loc[index, 'SVMl'] = accsvml[number]
        dataframe.loc[index, 'SVMnl'] = accsvmnl[number]
        dataframe.loc[index, 'Decision'] = accdes[number]
        dataframe.loc[index, 'Random'] = accrf[number]

    return dataframe

# Main Function
def selectKRegressionResult():
    dataset1 = pd.read_csv("prep.csv")
    df2 = pd.get_dummies(dataset1, drop_first=True)

    indep_X = df2.drop('classification_yes', axis=1)
    dep_Y = df2['classification_yes']

    kbest = selectkbest(indep_X, dep_Y, 5)

    acclin, accsvml, accsvmnl, accdes, accrf = [], [], [], [], []

    X_train, X_test, y_train, y_test = split_scalar(kbest, dep_Y)

    acclin.append(Linear(X_train, y_train, X_test, y_test))
    accsvml.append(svm_linear(X_train, y_train, X_test, y_test))
    accsvmnl.append(svm_NL(X_train, y_train, X_test, y_test))
    accdes.append(decision_tree(X_train, y_train, X_test, y_test))
    accrf.append(random_forest(X_train, y_train, X_test, y_test))

    result = selectk_regression(acclin, accsvml, accsvmnl, accdes, accrf)

    return result