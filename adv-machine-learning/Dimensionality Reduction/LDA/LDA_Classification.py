import pandas as pd

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


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
def cm_prediction(classifier, X_test, y_test):
    y_pred = classifier.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return acc, report, cm


# ---------------- MODELS ----------------
def logistic(X_train, y_train, X_test, y_test):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return cm_prediction(model, X_test, y_test)


def svm_linear(X_train, y_train, X_test, y_test):
    model = SVC(kernel='linear')
    model.fit(X_train, y_train)
    return cm_prediction(model, X_test, y_test)


def svm_rbf(X_train, y_train, X_test, y_test):
    model = SVC(kernel='rbf')
    model.fit(X_train, y_train)
    return cm_prediction(model, X_test, y_test)


def knn(X_train, y_train, X_test, y_test):
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)
    return cm_prediction(model, X_test, y_test)


def naive(X_train, y_train, X_test, y_test):
    model = GaussianNB()
    model.fit(X_train, y_train)
    return cm_prediction(model, X_test, y_test)


def decision_tree(X_train, y_train, X_test, y_test):
    model = DecisionTreeClassifier(criterion='entropy')
    model.fit(X_train, y_train)
    return cm_prediction(model, X_test, y_test)


def random_forest(X_train, y_train, X_test, y_test):
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    return cm_prediction(model, X_test, y_test)


# ---------------- MAIN LDA FUNCTION ----------------
def lda_classification_result():

    # Load dataset
    dataset = pd.read_csv("wine.csv")

    # Split features & target
    indep_X = dataset.drop('Customer_Segment', axis=1)
    dep_Y = dataset['Customer_Segment']

    # Apply LDA
    lda = LDA(n_components=2)
    X_lda = lda.fit_transform(indep_X, dep_Y)

    # Use transformed data directly
    indep_X = pd.DataFrame(X_lda, columns=['LD1', 'LD2'])

    # Train-test split
    X_train, X_test, y_train, y_test = split_scalar(indep_X, dep_Y)

    # Run all models
    results = {}

    results['Logistic'], _, _ = logistic(X_train, y_train, X_test, y_test)
    results['SVM Linear'], _, _ = svm_linear(X_train, y_train, X_test, y_test)
    results['SVM RBF'], _, _ = svm_rbf(X_train, y_train, X_test, y_test)
    results['KNN'], _, _ = knn(X_train, y_train, X_test, y_test)
    results['Naive Bayes'], _, _ = naive(X_train, y_train, X_test, y_test)
    results['Decision Tree'], _, _ = decision_tree(X_train, y_train, X_test, y_test)
    results['Random Forest'], _, _ = random_forest(X_train, y_train, X_test, y_test)

    # Convert to DataFrame
    result_df = pd.DataFrame(list(results.items()), columns=['Model', 'Accuracy'])

    return result_df


# ---------------- RUN ----------------
print(lda_classification_result())