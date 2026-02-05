from abc import abstractmethod, ABC

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame as SparkDataFrame


class ISparkRepository(ABC):
    @abstractmethod
    def get_spark_session(self) -> SparkSession:
        ...

    @abstractmethod
    def read_table(self, table_name: str) -> SparkDataFrame:
        ...

    @abstractmethod
    def read_sql(self, query: str) -> SparkDataFrame:
        ...

    @abstractmethod
    def to_pandas(self, df: SparkDataFrame) -> pd.DataFrame:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...
