import pandas as pd

from src.core.interfaces.data_aggregation_interface import IDataAggregationRepository


class DataAggregationRepository(IDataAggregationRepository):
    def get_all_table_data(self, table_name: str) -> pd.DataFrame:
        # сюда хз, мб тоже пайспарк
        pass

    def get_sakila_united_data(self) -> pd.DataFrame:
        # сюда впиндюрить pySpark
        pass