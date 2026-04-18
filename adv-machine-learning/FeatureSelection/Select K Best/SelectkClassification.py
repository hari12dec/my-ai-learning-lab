import pandas as pd
from sklearn.model_selection import train_test_split 
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# Feature Selection
def selectkbest(indep_X, dep_Y, n):
    test = SelectKBest(score_func=chi2, k=n)
    fit1 = test.fit(indep_X, dep_Y)
    selectk_features = fit1.transform(indep_X)
    return selectk_features

# Train Test Split + Scaling
def split_scalar(indep_X, dep_Y):
    X_train, X_test, y_train, y_test = train_test_split(
        indep_X, dep_Y, test_size=0.25, random_state=0
    )
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train, X_test, y_train, y_test

# Common Evaluation
def cm_prediction(classifier, X_test, y_test):
    y_pred = classifier.predict(X_test)

    from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
    
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return classifier, accuracy, report, X_test, y_test, cm

# Models
def logistic(X_train, y_train, X_test, y_test):
    classifier = LogisticRegression(random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)

def svm_linear(X_train, y_train, X_test, y_test):
    from sklearn.svm import SVC
    classifier = SVC(kernel='linear', random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)

def svm_NL(X_train, y_train, X_test, y_test):
    from sklearn.svm import SVC
    classifier = SVC(kernel='rbf', random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)

def naive_bayes(X_train, y_train, X_test, y_test):
    from sklearn.naive_bayes import GaussianNB
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)

def knn(X_train, y_train, X_test, y_test):
    from sklearn.neighbors import KNeighborsClassifier
    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)

def decision_tree(X_train, y_train, X_test, y_test):
    from sklearn.tree import DecisionTreeClassifier
    classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)

def random_forest(X_train, y_train, X_test, y_test):
    from sklearn.ensemble import RandomForestClassifier
    classifier = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)

# Accuracy Comparison Table
def selectk_Classification(acclog, accsvml, accsvmnl, accknn, accnav, accdes, accrf):
    dataframe = pd.DataFrame(
        index=['ChiSquare'],
        columns=['Logistic', 'SVMl', 'SVMnl', 'KNN', 'Naive', 'Decision', 'Random']
    )

    for number, index in enumerate(dataframe.index):
        dataframe.loc[index, 'Logistic'] = acclog[number]
        dataframe.loc[index, 'SVMl'] = accsvml[number]
        dataframe.loc[index, 'SVMnl'] = accsvmnl[number]
        dataframe.loc[index, 'KNN'] = accknn[number]
        dataframe.loc[index, 'Naive'] = accnav[number]
        dataframe.loc[index, 'Decision'] = accdes[number]
        dataframe.loc[index, 'Random'] = accrf[number]

    return dataframe

def selectk_ClassificationResult():
    import pandas as pd

    # Load Dataset
    dataset1 = pd.read_csv("prep.csv")
    df2 = pd.get_dummies(dataset1, drop_first=True)

    # Split features & target
    indep_X = df2.drop('classification_yes', axis=1)
    dep_Y = df2['classification_yes']

    # Feature Selection
    kbest = selectkbest(indep_X, dep_Y, 5)

    # Train-test split
    X_train, X_test, y_train, y_test = split_scalar(kbest, dep_Y)

    # Initialize accuracy lists
    acclog, accsvml, accsvmnl, accknn, accnav, accdes, accrf = [], [], [], [], [], [], []

    # Logistic Regression
    classifier, Accuracy, report, X_test, y_test, cm = logistic(X_train, y_train, X_test, y_test)
    acclog.append(Accuracy)

    # SVM Linear
    classifier, Accuracy, report, X_test, y_test, cm = svm_linear(X_train, y_train, X_test, y_test)
    accsvml.append(Accuracy)

    # SVM Non-Linear
    classifier, Accuracy, report, X_test, y_test, cm = svm_NL(X_train, y_train, X_test, y_test)
    accsvmnl.append(Accuracy)

    # KNN
    classifier, Accuracy, report, X_test, y_test, cm = knn(X_train, y_train, X_test, y_test)
    accknn.append(Accuracy)

    # Naive Bayes
    classifier, Accuracy, report, X_test, y_test, cm = naive_bayes(X_train, y_train, X_test, y_test)
    accnav.append(Accuracy)

    # Decision Tree
    classifier, Accuracy, report, X_test, y_test, cm = decision_tree(X_train, y_train, X_test, y_test)
    accdes.append(Accuracy)

    # Random Forest (you missed this)
    classifier, Accuracy, report, X_test, y_test, cm = random_forest(X_train, y_train, X_test, y_test)
    accrf.append(Accuracy)

    # Final result table
    result = selectk_Classification(acclog, accsvml, accsvmnl, accknn, accnav, accdes, accrf)

    return result