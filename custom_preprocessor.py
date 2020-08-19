from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
class custom_preprocessor( BaseEstimator, TransformerMixin):
    
    def fit(self, X, y = None ):
        self.categorical_columns = X.select_dtypes('object').columns
        self.numeric_columns = X.select_dtypes('number').columns
        return self
    
    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)
    def transform(self, X, y=None):
        res = X.copy()
        ##custom
        categorical_columns = res.select_dtypes('object').columns
        numeric_columns = res.select_dtypes('number').columns
        
        for column in set(self.categorical_columns) - set(categorical_columns) :
            res[column] = np.nan
        for column in set(self.numeric_columns) - set(numeric_columns) :
            res[column] = np.nan
        for column in self.categorical_columns:
            res[column] = res[column].fillna('No')
        for column in self.numeric_columns:
            res[column] = res[column].fillna(0)
        return res