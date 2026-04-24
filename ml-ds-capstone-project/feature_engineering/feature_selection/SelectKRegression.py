import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression

# Feature Selection
def selectkbest(indep_X, dep_Y, k):
    selector = SelectKBest(score_func=f_regression, k=k)
    X_new = selector.fit_transform(indep_X, dep_Y)
    selected_features = indep_X.columns[selector.get_support()]
    return X_new, selected_features

# Train/Test Split + Scaling
def split_scale(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train, X_test, y_train, y_test

# R2 Evaluation
def r2_score_model(model, X_test, y_test):
    from sklearn.metrics import r2_score
    y_pred = model.predict(X_test)
    return r2_score(y_test, y_pred)

# Models
def run_models(X_train, y_train, X_test, y_test):
    from sklearn.linear_model import LinearRegression
    from sklearn.svm import SVR
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.ensemble import RandomForestRegressor

    results = {}

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=0,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    results["RFR"] = r2_score_model(model, X_test, y_test)

    model = GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.03,
        max_depth=5,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=0
    )
    model.fit(X_train, y_train)
    results["GBR"] = r2_score_model(model, X_test, y_test)
   
    # Linear
    model = LinearRegression()
    model.fit(X_train, y_train)
    results["Linear"] = r2_score_model(model, X_test, y_test)

    # SVM Linear
    model = SVR(kernel='linear')
    model.fit(X_train, y_train)
    results["SVMl"] = r2_score_model(model, X_test, y_test)

    # SVM RBF
    model = SVR(kernel='rbf')
    model.fit(X_train, y_train)
    results["SVMnl"] = r2_score_model(model, X_test, y_test)

    # Decision Tree
    model = DecisionTreeRegressor(random_state=0)
    model.fit(X_train, y_train)
    results["Decision"] = r2_score_model(model, X_test, y_test)

    # Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)
    results["Random"] = r2_score_model(model, X_test, y_test)

    return results

# Main Function
def selectKRegressionResult(dataset, target, k=10):

    # Encode only if needed
    if dataset.select_dtypes(include='object').shape[1] > 0:
        df = pd.get_dummies(dataset, drop_first=True)
    else:
        df = dataset.copy()

    # Handle missing values
    df = df.fillna(df.median(numeric_only=True))

    # Split features and target
    X = df.drop(target, axis=1)
    y = df[target]

    # Feature Selection
    X_new, selected_features = selectkbest(X, y, k)

    print("Selected Features:", list(selected_features))

    # Split + Scale
    X_train, X_test, y_train, y_test = split_scale(X_new, y)

    # Run models
    results = run_models(X_train, y_train, X_test, y_test)

    # Convert to DataFrame
    result_df = pd.DataFrame([results], index=["Regression"])

    return result_df