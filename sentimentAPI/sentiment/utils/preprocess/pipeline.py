#coding:utf8
"""

"""

from __future__ import absolute_import
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin



class SplitText(BaseEstimator, TransformerMixin):
    """
    It's a sklearn estimator that can extract features from text.
    """

    def __init__(self, split=False):
        # `split` method can use string split method to cut string, if it's True
        self.split = split


    def fit(self, X, y=None):
        return self

    
    def transform(self, X):
        if self.split:
            if isinstance(X, pd.Series):
                return X.str.split(" ")
            else:
                raise TypeError(f"Can't Support {type(X)}. String series is supported")
        else:
            return X