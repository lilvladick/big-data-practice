from typing import Annotated

import pandas as pd
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException

from src.core.services.data_aggregation_service import DataAggregationService
from src.core.services.data_analysis_service import DataAnalysisService

router = APIRouter(route_class=DishkaRoute)

@router.get("/say_hello")
def say_hello():
    return {"hello": "world"}

# валидации пока выносить не хочу

@router.get("/{column}")
def get_univariate_column_analysis(column: str, aggregation_service: Annotated[DataAggregationService, FromDishka()]):
    df = aggregation_service.get_dataframe()
    _validate_column(df, column)
    try:
        result = DataAnalysisService.univariate_analysis(df, column)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/categorial/{column}")
def get_categorial_analysis(column: str, aggregation_service: Annotated[DataAggregationService, FromDishka()]):
    df = aggregation_service.get_dataframe()
    _validate_column(df, column, is_categorical=True)
    try:
        result = DataAnalysisService.categorical_analysis(df, column)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


def _validate_column(df: pd.DataFrame, column: str, is_categorical: bool = False):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail=f"Column '{column}' not found.")

    if not is_categorical and not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail=f"Column '{column}' must be numeric.")
