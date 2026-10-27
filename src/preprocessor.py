import pandas as pd
import numpy as np
import pickle
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.config import NUMERIC_FEATURES, CATEGORICAL_FEATURES, PREPROCESSOR_PATH

class NetworkPreprocessor:
    def __init__(self):
        # OneHotEncoder handles unknown categories by placing all zeros for them,
        # which is robust for live network streams
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), NUMERIC_FEATURES),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES)
            ]
        )
        self.feature_names = []
        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        """Fits the scaler and encoder on baseline data."""
        # Ensure only the needed features are passed in
        X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
        self.preprocessor.fit(X)
        self.is_fitted = True
        
        # Extract feature names for SHAP explanations
        num_cols = NUMERIC_FEATURES
        cat_encoder = self.preprocessor.named_transformers_['cat']
        cat_cols = []
        for col, categories in zip(CATEGORICAL_FEATURES, cat_encoder.categories_):
            cat_cols.extend([f"{col}_{cat}" for cat in categories])
        self.feature_names = num_cols + cat_cols

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transforms a DataFrame of raw network flows into scaled feature arrays."""
        if not self.is_fitted:
            raise ValueError("Preprocessor has not been fitted yet!")
        X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
        return self.preprocessor.transform(X)

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        """Fits and transforms in one step."""
        self.fit(df)
        return self.transform(df)

    def get_feature_names(self) -> list:
        """Returns the list of processed feature names (after one-hot encoding)."""
        return self.feature_names

    def save(self, filepath: str = PREPROCESSOR_PATH):
        """Saves the preprocessor to disk."""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filepath: str = PREPROCESSOR_PATH) -> 'NetworkPreprocessor':
        """Loads a preprocessor from disk."""
        with open(filepath, 'rb') as f:
            return pickle.load(f)
