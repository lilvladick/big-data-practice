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
