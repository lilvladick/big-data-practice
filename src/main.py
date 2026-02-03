import uvicorn
from fastapi import FastAPI

from src.presentation.routers import multivariate
from src.presentation.routers import univariate

app = FastAPI()

app.include_router(multivariate.router, prefix="/multivariate", tags=["multivariate"])
app.include_router(univariate.router, prefix="/univariate", tags=["univariate"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)