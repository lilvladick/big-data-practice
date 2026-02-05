from pathlib import Path
from typing import Dict
import pandas as pd

from src.core.interfaces.data_aggregation_interface import IDataAggregationRepository


class DataAggregationService:
    def __init__(self, data_aggregation_repository: IDataAggregationRepository, cache_dir: str = "./data_cache"):
        self.data_aggregation_repository = data_aggregation_repository
        self.cache_dir = cache_dir
        self.user_temp_dirs: Dict[str, Path] = {}

    # чисто для админов функция, чтобы создавать дамб бдшки спарком, чтобы не юзать спарк всегда
    def load_base_csv(self, force_refresh: bool = False) -> pd.DataFrame:
        csv_path = Path(self.cache_dir) / "sakila_united_data.csv"
        if csv_path.exists() and not force_refresh:
            return pd.read_csv(csv_path)
        df = self.data_aggregation_repository.get_sakila_united_data()
        df.to_csv(csv_path, index=False)
        return df

    # вообще я сначала думал сделать тут для каждого юзера свой csv чтобы можно было с ними играть,
    # но пока что мне лень

    @staticmethod
    def univariate_analysis(df: pd.DataFrame, column: str) -> Dict:
        return {
            'describe': df[column].describe().to_dict(),
            'missing': df[column].isnull().sum(),
            'unique': df[column].nunique(),
            'mode': df[column].mode().tolist(),
            'histogram_bins': pd.cut(df[column].dropna(), bins=10).value_counts().to_dict()
        }

    @staticmethod
    def categorical_analysis(df: pd.DataFrame, column: str) -> pd.DataFrame:
        return (df[column].value_counts()
                .reset_index()
                .rename(columns={column: 'count', 'index': column}))

    # TODO: многомерный анализ да да снизу потом