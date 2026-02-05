import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.infrastructure.dependency_injection import container
from src.presentation.routers import multivariate, users, univariate, auth, admin

app = FastAPI()

setup_dishka(container=container, app=app)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["authorization"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(multivariate.router, prefix="/multivariate", tags=["multivariate"])
app.include_router(univariate.router, prefix="/univariate", tags=["univariate"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
