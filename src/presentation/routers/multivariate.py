from typing import Annotated, List

import pandas as pd
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status, Query

from src.core.services.data_aggregation_service import DataAggregationService
from src.core.services.data_analysis_service import DataAnalysisService

router = APIRouter(route_class=DishkaRoute)


@router.get("/say_hello")
def say_hello():
    return {"hello": "world"}


# валидации пока выносить не хочу

@router.get("/")
def get_multivariate_column_analysis(aggregation_service: Annotated[DataAggregationService, FromDishka()],
                                     columns: List[str] = Query(...)):
    df = aggregation_service.get_dataframe()
    _validate_columns(df, columns)
    try:
        result = DataAnalysisService.multivariate_analysis(df, columns)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")


@router.get("/knn_class/{target_column}")
async def knn_classification_analysis(aggregation_service: Annotated[DataAggregationService, FromDishka()],
                                      target_column: str, feature_columns: List[str] = Query(...),
                                      columns: List[str] = Query([]), k: int = Query(5, ge=1, le=50),
                                      test_size: float = Query(0.25, ge=0.1, le=0.5)):
    df = aggregation_service.get_dataframe()
    _validate_columns(df, columns, is_categorical=True)
    try:
        result = DataAnalysisService.knn_classification(df, feature_columns, target_column, k, test_size)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")


def _validate_columns(df: pd.DataFrame, columns: List[str], is_categorical: bool = False):
    for column in columns:
        if column not in df.columns:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Column '{column}' not found.")

        if not is_categorical and not pd.api.types.is_numeric_dtype(df[column]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Column '{column}' must be numeric.")
