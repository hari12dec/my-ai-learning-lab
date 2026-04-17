# =========================
# PCA + Classification (All Models)
# =========================

import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

# =========================
# PCA Function
# =========================
def apply_pca(indep_X, n):
    pca = PCA(n_components=n)
    pca_features = pca.fit_transform(indep_X)
    return pca_features

# =========================
# Train Test Split + Scaling
# =========================
def split_scalar(indep_X, dep_Y):
    X_train, X_test, y_train, y_test = train_test_split(
        indep_X, dep_Y, test_size=0.25, random_state=0
    )
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    return X_train, X_test, y_train, y_test

# =========================
# Common Evaluation
# =========================
def cm_prediction(classifier, X_test, y_test):
    y_pred = classifier.predict(X_test)

    from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
    
    cm = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return classifier, accuracy, report, X_test, y_test, cm

# =========================
# Models
# =========================
def logistic(X_train, y_train, X_test, y_test):
    classifier = LogisticRegression(multi_class='auto', solver='lbfgs', max_iter=1000)
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

# =========================
# PCA Accuracy Table
# =========================
def pca_Classification(acclog, accsvml, accsvmnl, accknn, accnav, accdes, accrf):
    dataframe = pd.DataFrame(
        index=['PCA'],
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

# =========================
# Main Function
# =========================
def pca_ClassificationResult():

    # Load Dataset
    dataset1 = pd.read_csv("Wine.csv")

    indep_X = dataset1.iloc[:, 1:]
    dep_Y = dataset1.iloc[:, 0]

    dep_Y = dep_Y.astype(int)
    
    X_train, X_test, y_train, y_test = split_scalar(indep_X, dep_Y)

    from sklearn.decomposition import PCA
    pca = PCA(n_components=5)

    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    # Accuracy lists
    acclog, accsvml, accsvmnl, accknn, accnav, accdes, accrf = [], [], [], [], [], [], []

    # Logistic
    _, acc, _, _, _, _ = logistic(X_train, y_train, X_test, y_test)
    acclog.append(acc)

    # SVM Linear
    _, acc, _, _, _, _ = svm_linear(X_train, y_train, X_test, y_test)
    accsvml.append(acc)

    # SVM Non-linear
    _, acc, _, _, _, _ = svm_NL(X_train, y_train, X_test, y_test)
    accsvmnl.append(acc)

    # KNN
    _, acc, _, _, _, _ = knn(X_train, y_train, X_test, y_test)
    accknn.append(acc)

    # Naive Bayes
    _, acc, _, _, _, _ = naive_bayes(X_train, y_train, X_test, y_test)
    accnav.append(acc)

    # Decision Tree
    _, acc, _, _, _, _ = decision_tree(X_train, y_train, X_test, y_test)
    accdes.append(acc)

    # Random Forest
    _, acc, _, _, _, _ = random_forest(X_train, y_train, X_test, y_test)
    accrf.append(acc)

    # Final Table
    result = pca_Classification(acclog, accsvml, accsvmnl, accknn, accnav, accdes, accrf)

    return result
    