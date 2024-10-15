from fastapi import APIRouter, HTTPException
from app.services.db_crud import get_chat_history

docu_history_router = APIRouter()


@docu_history_router.get("/history/{doc_uuid}")
def get_history(doc_uuid: str):
    history = get_chat_history(doc_uuid)
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return history

