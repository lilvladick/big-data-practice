from abc import abstractmethod, ABC

import pandas as pd


class IDataAggregationRepository(ABC):
    @abstractmethod
    def get_all_table_data(self, table_name: str) -> pd.DataFrame:
        ...

    @abstractmethod
    def get_sakila_united_data(self) -> pd.DataFrame:
        ...
