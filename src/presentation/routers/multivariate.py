from fastapi import APIRouter

router = APIRouter()

@router.get("/say_hello")
def say_hello():
    return {"hello": "world"}