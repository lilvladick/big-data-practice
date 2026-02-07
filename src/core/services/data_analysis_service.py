from typing import Dict
import pandas as pd


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

    # TODO: многомерный анализ да да снизу потом
