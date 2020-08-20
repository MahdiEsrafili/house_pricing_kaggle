from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import bisect

class ModifiedLabelEncoder(LabelEncoder):

    def fit_transform(self, X,y=None):
        return self.fit(X, y).transform(X)
    
    def fit(self, X, y=None):
        res = X.copy()
        categorical_columns = res.select_dtypes('object').columns
        self.encoders = dict()
        for column in categorical_columns:
            le = LabelEncoder().fit(res[column])
            le_classes = le.classes_.tolist()
            bisect.insort_left(le_classes, 'No')
            le.classes_ = le_classes
            self.encoders[column]  = le
        return self
    
    def transform(self,X, y=None):
        res = X.copy()
        categorical_columns = res.select_dtypes('object').columns
        for column in categorical_columns:
            le = LabelEncoder()
            le.classes_ = self.encoders[column].classes_
            res.loc[:,column] = res.loc[:,column].map(lambda x:'No' if x not in le.classes_ else x)
            res.loc[:,column] = le.transform(res[column]).reshape(-1, 1)
        return res