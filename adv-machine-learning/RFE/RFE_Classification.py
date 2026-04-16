import pandas as pd
from sklearn.model_selection import train_test_split 
import time
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
import pickle
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier   
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler

def rfeFeature(indep_X, dep_Y, n):
    rfelist = []

    sc = StandardScaler()
    indep_X = sc.fit_transform(indep_X)

    log_model = LogisticRegression(max_iter=2000)
    RF = RandomForestClassifier(n_estimators=10, random_state=0)
    DT = DecisionTreeClassifier(random_state=0)
    svc_model = SVC(kernel='linear')

    rfemodellist = [log_model, svc_model, RF, DT]

    for model in rfemodellist:
        log_rfe = RFE(estimator=model, n_features_to_select=n)
        log_fit = log_rfe.fit(indep_X, dep_Y)

        log_rfe_feature = log_fit.transform(indep_X)
        rfelist.append(log_rfe_feature)

    return rfelist
    

def split_scalar(indep_X,dep_Y):
        X_train, X_test, y_train, y_test = train_test_split(indep_X, dep_Y, test_size = 0.25, random_state = 0)
        #X_train, X_test, y_train, y_test = train_test_split(indep_X,dep_Y, test_size = 0.25, random_state = 0)
        
        #Feature Scaling
        #from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        
        return X_train, X_test, y_train, y_test
    
def cm_prediction(classifier, X_test, y_test):
    y_pred = classifier.predict(X_test)

    from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

    cm = confusion_matrix(y_test, y_pred)
    Accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return classifier, Accuracy, report, cm

def logistic(X_train, y_train, X_test, y_test):
    classifier = LogisticRegression(random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)


def svm_linear(X_train, y_train, X_test, y_test):
    classifier = SVC(kernel='linear', random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)


def svm_NL(X_train, y_train, X_test, y_test):
    classifier = SVC(kernel='rbf', random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)


def knn(X_train, y_train, X_test, y_test):
    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)


def Navie(X_train, y_train, X_test, y_test):
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)


def Decision(X_train, y_train, X_test, y_test):
    classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)


def random(X_train, y_train, X_test, y_test):
    classifier = RandomForestClassifier(n_estimators=10, random_state=0)
    classifier.fit(X_train, y_train)
    return cm_prediction(classifier, X_test, y_test)
    

def rfe_classification(acclog,accsvml,accsvmnl,accknn,accnav,accdes,accrf): 
    
    rfedataframe=pd.DataFrame(index=['Logistic','SVC','Random','DecisionTree'],columns=['Logistic','SVMl','SVMnl',
                                                                                        'KNN','Navie','Decision','Random'])

    for number,idex in enumerate(rfedataframe.index):
        
        rfedataframe['Logistic'][idex]=acclog[number]       
        rfedataframe['SVMl'][idex]=accsvml[number]
        rfedataframe['SVMnl'][idex]=accsvmnl[number]
        rfedataframe['KNN'][idex]=accknn[number]
        rfedataframe['Navie'][idex]=accnav[number]
        rfedataframe['Decision'][idex]=accdes[number]
        rfedataframe['Random'][idex]=accrf[number]
    return rfedataframe



def rfe_classification_result():
    dataset1 = pd.read_csv("prep.csv")

    df2 = pd.get_dummies(dataset1, drop_first=True)

    indep_X = df2.drop('classification_yes', axis=1)
    dep_Y = df2['classification_yes']

    rfelist = rfeFeature(indep_X, dep_Y, 3)

    acclog, accsvml, accsvmnl, accknn, accnav, accdes, accrf = [], [], [], [], [], [], []

    for i in rfelist:
        X_train, X_test, y_train, y_test = split_scalar(i, dep_Y)

        _, acc, _, _ = logistic(X_train, y_train, X_test, y_test)
        acclog.append(acc)

        _, acc, _, _ = svm_linear(X_train, y_train, X_test, y_test)
        accsvml.append(acc)

        _, acc, _, _ = svm_NL(X_train, y_train, X_test, y_test)
        accsvmnl.append(acc)

        _, acc, _, _ = knn(X_train, y_train, X_test, y_test)
        accknn.append(acc)

        _, acc, _, _ = Navie(X_train, y_train, X_test, y_test)
        accnav.append(acc)

        _, acc, _, _ = Decision(X_train, y_train, X_test, y_test)
        accdes.append(acc)

        _, acc, _, _ = random(X_train, y_train, X_test, y_test)
        accrf.append(acc)

    result = rfe_classification(
        acclog, accsvml, accsvmnl, accknn, accnav, accdes, accrf
    )

    return result