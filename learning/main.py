# -*- coding: utf-8 -*-
import category_encoders as ce
import os
import pandas as pd
from sklearn.model_selection import train_test_split


def train_model():
    data_dir = "./model"
    data_file = os.path.join(data_dir, "base_dataV1.0.xlsx")

    dt = pd.read_excel(data_file, sheetname='Sheet2').replace({'无': '否'})

    X = dt.drop(columns='purchase')
    y = dt['purchase'].copy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    ohe = ce.OneHotEncoder(handle_unknown='ignore', use_cat_names=True)
    X_train_ohe = ohe.fit_transform(X_train)
    X_train_ohe.head()

    X_test_ohe = ohe.transform(X_test)
    X_test_ohe.head()

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

    from sklearn.ensemble import RandomForestClassifier

    rf = Pipeline(steps=[('preprocessor', preprocessor),
                         ('classifier', RandomForestClassifier())])

    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC, LinearSVC, NuSVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier

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

    import pickle

    filehandler = open(b"./model/pipe_model.pkl", "wb")
    pickle.dump(pipe, filehandler)
    filehandler.close()
    print('-------------------------Model train finished.---------------------------------')
