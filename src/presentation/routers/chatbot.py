from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, logger, status, WebSocket, WebSocketDisconnect
from src.infrastructure.dependency_injection import container as dishka_container
from src.infrastructure.services.data_science_rag_service import DataScienceRAGService

router = APIRouter(route_class=DishkaRoute)

@router.get("/say_hello")
def say_hello():
    return {"hello": "world"}

@router.post("/ask")
def ask_question(
    question: str,
    rag_service: Annotated[DataScienceRAGService, FromDishka()]
):
    try:
        answer = rag_service.ask(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.websocket("/ws")
async def stream_chatbot(websocket: WebSocket):
    await websocket.accept()
    
    rag_service = await dishka_container.get(DataScienceRAGService)

    try:
        while True:
            question = await websocket.receive_text()
            async for chunk in rag_service.stream_ask(question):
                await websocket.send_text(chunk)

            await websocket.send_text("[DONE]")

    except WebSocketDisconnect:
          pass
    except Exception as e:
        await websocket.send_text(f"[ERROR] {str(e)}")
    finally:
        await websocket.close()