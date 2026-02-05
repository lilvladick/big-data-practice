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

        unique_vals = series.dropna().nunique()
        bins = min(10, unique_vals) if unique_vals > 1 else 1

        return {
            'describe': series.describe().to_dict(),
            'missing': int(series.isnull().sum()),
            'unique': int(series.nunique()),
            'mode': series.mode().tolist() or [None],
            'histogram_bins': (
                pd.cut(series.dropna(), bins=bins).value_counts().to_dict()
                if unique_vals > 1 else {f"single_value_{series.dropna().iloc[0]}": len(series.dropna())}
            )
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
