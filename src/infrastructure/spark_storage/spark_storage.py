from typing import Optional

import pandas as pd
from pyspark.sql import DataFrame as SparkDataFrame, SparkSession
from src.core.interfaces.spark_interface import ISparkRepository


class SparkStorage(ISparkRepository):
    def __init__(self, jdbc_url: str, jdbc_properties: dict, app_name:str = "DataPlayground", master: str = "local[*]"):
        self.app_name = app_name
        self.jdbc_url = jdbc_url
        self.jdbc_properties = jdbc_properties
        self.master = master
        self.spark: Optional[SparkSession] = None
        self._init_spark()

    def _init_spark(self) -> None:
        if self.spark is None:
            self.spark = (SparkSession.builder.appName(self.app_name).master(self.master)
                          .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
                          .config("spark.sql.adaptive.enabled", "true")
                          .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
                          .getOrCreate())

    def get_spark_session(self) -> SparkSession:
        self._init_spark()
        return self.spark

    def read_table(self, table_name: str) -> SparkDataFrame:
        spark = self.get_spark_session()
        return (spark.read.format("jdbc")
                .option("url", self.jdbc_url)
                .option("dbtable", table_name)
                .option("driver", "org.postgresql.Driver")
                .options(**self.jdbc_properties)
                .load())

    def read_sql(self, query: str) -> SparkDataFrame:
        spark = self.get_spark_session()
        return (spark.read.format("jdbc")
                .option("url", self.jdbc_url)
                .option("dbtable", f"({query}) AS subquery")
                .option("driver", "org.postgresql.Driver")
                .options(**self.jdbc_properties)
                .load())

    def to_pandas(self, df: SparkDataFrame) -> pd.DataFrame:
        return df.toPandas()

    def stop(self) -> None:
        if self.spark:
            self.spark.stop()