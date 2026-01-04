import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA

## Log: Transform amb MinMax, Transformacions logarítmiques. El tractament d'outliers es fa amb clipping.
# La imputació de valors faltants es fa amb la mediana de cada columna.

class Preprocessing:
    extreme_cols = ["koi_period",
        "koi_period_err1",
        "koi_period_err2",
        "koi_prad",
        "koi_prad_err1",
        "koi_prad_err2",
        "koi_insol",
        "koi_insol_err1",
        "koi_srad",
        "koi_srad_err1",
        "koi_srad_err2",
        "koi_depth",
        "koi_depth_err1",
        "koi_depth_err2"
    ]
    skewed_cols = [
        "koi_impact_err2",
        "koi_impact_err1",
        "koi_impact",
        
        "koi_duration",
        "koi_duration_err1",
        "koi_duration_err2",
        "koi_teq",
        "koi_model_snr"
    ]

    def __init__(self):
        self.normalizer : None | MinMaxScaler = None
        self.imputer : None | SimpleImputer = None

    def transform(self, X: pd.DataFrame) -> pd.DataFrame: 
        assert self.normalizer is not None, "Normalizer has not been fitted. Call fit_transform first."
        assert self.imputer is not None, "Imputer has not been fitted. Call fit_transform first."

        X_imputed = pd.DataFrame(self.imputer.transform(X), columns=X.columns)
        X_rescaled = self.rescalaIpositivitza(X_imputed)
        
        X_normalized = pd.DataFrame(self.normalizer.transform(X_rescaled), columns=X.columns)
        return X_normalized
    
    def fit_transform(self, normalizer: MinMaxScaler, imputer: SimpleImputer, X_train: pd.DataFrame) -> pd.DataFrame:
        self.normalizer = normalizer
        self.imputer = imputer
        X_train_imputed = pd.DataFrame(self.imputer.fit_transform(X_train), columns=X_train.columns)
        X_train_rescaled = self.rescalaIpositivitza(X_train_imputed)
        X_train_normalized = pd.DataFrame(self.normalizer.fit_transform(X_train_rescaled), columns=X_train.columns)
        return X_train_normalized

    def rescalaIpositivitza(self, X: pd.DataFrame) -> pd.DataFrame:
        assert set(self.skewed_cols).issubset(X.columns), \
            "Some skewed columns are missing in the input data."
        assert set(self.extreme_cols).issubset(X.columns), \
            "Some extreme columns are missing in the input data."

        X_rescaled = X.copy().abs()
        X_rescaled[Preprocessing.extreme_cols] = X_rescaled[Preprocessing.extreme_cols].clip(upper=X_rescaled[Preprocessing.extreme_cols].quantile(0.99), axis = 1)
        X_rescaled[Preprocessing.extreme_cols + Preprocessing.skewed_cols] = \
            np.log1p(X_rescaled[Preprocessing.extreme_cols + Preprocessing.skewed_cols])
        return X_rescaled

    

