# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 13:29:42 2019
#https://scikit-learn.org/stable/modules/preprocessing.html#encoding-categorical-features
#https://medium.com/hugo-ferreiras-blog/dealing-with-categorical-features-in-machine-learning-1bb70f07262d
#https://www.kaggle.com/c/titanic/discussion/5379
@author: WON4SZH
"""

import category_encoders as ce
import os
import pandas as pd
from sklearn.model_selection import train_test_split

data_dir = "..\model"
data_file = os.path.join(data_dir, "三焦点项目数据V1.0.xlsx")

dt = pd.read_excel(data_file, sheetname='Sheet2').replace({'无': '否'})
dt.dtypes

X = dt.drop(columns='purchase')
y = dt['purchase'].copy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# on-host encodeprepare_pred_data
ohe = ce.OneHotEncoder(handle_unknown='ignore', use_cat_names=True)
X_train_ohe = ohe.fit_transform(X_train)
X_train_ohe.head()

X_test_ohe = ohe.transform(X_test)
X_test_ohe.head()

##
# refer; https://medium.com/vickdata/a-simple-guide-to-scikit-learn-pipelines-4ac0d974bdcf
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

numeric_features = dt.select_dtypes(include=['int64', 'float64']).columns
categorical_features = dt.select_dtypes(include=['object']).drop(['purchase'], axis=1).columns

from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# fit
from sklearn.ensemble import RandomForestClassifier

rf = Pipeline(steps=[('preprocessor', preprocessor),
                     ('classifier', RandomForestClassifier())])

rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

# Model selection
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="rbf", C=0.025, probability=True),
    NuSVC(probability=True),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    AdaBoostClassifier(),
    GradientBoostingClassifier()
]

for classifier in classifiers:
    pipe = Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', classifier)])
    pipe.fit(X_train, y_train)

# search best for rf
param_grid = {
    'classifier__n_estimators': [200, 500],
    'classifier__max_features': ['auto', 'sqrt', 'log2'],
    'classifier__max_depth': [4, 5, 6, 7, 8],
    'classifier__criterion': ['gini', 'entropy']
}

from sklearn.model_selection import GridSearchCV

CV = GridSearchCV(rf, param_grid, n_jobs=1)

CV.fit(X_train, y_train)

import numpy as np


def prepare_pred_data(v_list):
    colnames = ['X1_age', 'X2_gender', 'X3_edu', 'X4_Zeisis', 'X5_insurance', 'X6_qualification', 'X7_acquaintance',
                'X8_shotsight', 'X9_income', 'X10_intemperance']
    colnames = np.array(colnames)
    dt_t = pd.DataFrame(np.array(v_list).reshape(1, 10), columns=colnames).replace({'无': '否'})
    return dt_t

def main():
    import pickle

    filehandler = open(b"..\\model\\pipe_model.pkl", "wb")
    pickle.dump(pipe, filehandler)
    filehandler = open(b"..\\model\\prepare_pred.pkl", "wb")
    pickle.dump(prepare_pred_data, filehandler)
    filehandler.close()

main()

