from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder


class DataAnalysisService:
    @staticmethod
    def univariate_analysis(df: pd.DataFrame, column: str) -> Dict:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")

        series = df[column]

        if not pd.api.types.is_numeric_dtype(series):
            raise TypeError(f"Column '{column}' must be numeric for univariate analysis")

        clean_series = series.dropna()
        unique_vals = clean_series.nunique()
        bins = min(10, unique_vals) if unique_vals > 1 else 1

        if unique_vals > 1:
            hist = (pd.cut(clean_series, bins=bins).value_counts().sort_index())

            histogram_bins = {str(interval): int(count) for interval, count in hist.items()}
        else:
            value = clean_series.iloc[0] if not clean_series.empty else None
            histogram_bins = {f"single_value_{value}": int(len(clean_series))}

        return {
            "describe": series.describe().to_dict(),
            "missing": int(series.isnull().sum()),
            "unique": int(series.nunique()),
            "mode": series.mode().astype(float).tolist() or [None],
            "histogram_bins": histogram_bins,
        }

    @staticmethod
    def categorical_analysis(df: pd.DataFrame, column: str) -> Dict:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")

        value_counts = df[column].value_counts()
        return {
            'value_counts': value_counts.to_dict(),
            'top_n': value_counts.head(10).to_dict(),
            'missing': int(df[column].isnull().sum()),
            'unique': int(df[column].nunique())
        }

    @staticmethod
    def multivariate_analysis(df: pd.DataFrame, columns: List[str]) -> Dict:
        for col in columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found")
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise TypeError(f"Column '{col}' must be numeric for multivariate analysis")

        sub_df = df[columns].dropna()
        if sub_df.empty:
            raise ValueError("No data available after dropping missing values")

        correlation = sub_df.corr().to_dict()
        covariance = sub_df.cov().to_dict()

        return {
            "correlation": correlation,
            "covariance": covariance,
            "num_observations": len(sub_df),
            "columns": columns
        }

    @staticmethod
    def knn_classification(df: pd.DataFrame, feature_columns: List[str], target_column: str, k: int = 5,
                           test_size: float = 0.25, random_state: int = 42, scale_features: bool = True,
                           weights: str = "uniform", metric: str = "euclidean") -> Dict:

        required_cols = feature_columns + [target_column]
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {', '.join(missing)}")

        sub_df = df[required_cols].dropna().copy()
        if len(sub_df) < 20:
            raise ValueError(f"Too little data after dropna: {len(sub_df)} rows")

        if sub_df[target_column].nunique() < 2:
            raise ValueError(f"Target variable '{target_column}' has less than 2 unique values")

        X = sub_df[feature_columns].values.astype(np.float64)
        y_raw = sub_df[target_column]

        if not np.issubdtype(y_raw.dtype, np.number):
            le = LabelEncoder()
            y = le.fit_transform(y_raw)
            class_names = le.classes_.tolist()
        else:
            y = y_raw.values.astype(int)
            class_names = np.unique(y).tolist()

        scaler = None
        if scale_features:
            scaler = StandardScaler()
            X = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state,
            stratify=y
        )

        knn = KNeighborsClassifier(
            n_neighbors=k,
            weights=weights,
            metric=metric,
            n_jobs=-1
        )
        knn.fit(X_train, y_train)

        y_pred = knn.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        result = {
            "accuracy": float(acc),
            "classification_report": report,
            "confusion_matrix": cm,
            "n_train": len(X_train),
            "n_test": len(X_test),
            "k": k,
            "target_column": target_column,
            "feature_columns": feature_columns,
            "class_names": class_names,
            "weights": weights,
            "metric": metric,
            "model": knn,
        }

        if scaler:
            result["scaler"] = scaler

        return result
