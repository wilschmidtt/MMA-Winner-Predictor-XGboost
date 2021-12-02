import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score


def imputeNumeric(X):
    '''
    Impute missing numeric values with mean of column
    '''

    # Move categorical columns 15 and 35 to front of array
    X[:,[0, 15]] = X[:,[15, 0]]
    X[:,[1, 35]] = X[:,[35, 1]]

    # Impute missing valus
    imputer = SimpleImputer(missing_values = np.nan, strategy = 'mean')
    imputer = imputer.fit(X[:, 2:40])
    X[:, 2:40] = imputer.transform(X[:, 2:40])

    return X


def imputeCategorical(X):
    '''
    Impute missing categorical values with most frequent value in column
    '''

    imputer = SimpleImputer(strategy="most_frequent")
    X[:, [0,1]] = imputer.fit_transform(X[:, [0,1]])

    return X


def oneHotEncode(X):
    '''
    Encoding categorical data
    '''

    labelencoder = LabelEncoder()
    X[:, 0] = labelencoder.fit_transform(X[:, 0])
    X[:, 1] = labelencoder.fit_transform(X[:, 1])
    enc = OneHotEncoder(handle_unknown='ignore')
    X_enc = enc.fit_transform(X[:, [0,1]]).toarray()
    X_enc = np.delete(X_enc, [0,2,5,7], 1)
    X = np.delete(X, [0,1], 1)
    X = np.concatenate((X, X_enc), axis=1)

    return X

def fitModel(X_train, X_test, y_train, y_test):
    '''
    Fitting XGBoost to the Training Set
    '''
    classifier = XGBClassifier()
    classifier.fit(X_train, y_train)

    return classifier

def crossValidation(classifier, X_train, y_train):
    '''
    Applying k-Fold Cross Validation
    '''

    accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
    print(f"\nXGBoost Accuracy: {accuracies.mean()}")
    print(f"XGBoost Standard Deviation: {accuracies.std()}")

def main(path):
    '''
    Executes main logic and calls all supporting functions
    '''
    
    df = pd.read_csv(path)
    X = df.iloc[:, 2:42].values
    y = df.iloc[:, 42].values

    X = imputeNumeric(X)
    X = imputeCategorical(X)
    X = oneHotEncode(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    classifier = fitModel(X_train, X_test, y_train, y_test)
    y_pred = classifier.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    crossValidation(classifier, X_train, y_train)

if __name__ == "__main__":
    # Supply path to UFCdata.csv below
    main('PATH HERE')