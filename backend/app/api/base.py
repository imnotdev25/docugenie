from fastapi import APIRouter


base_router = APIRouter()

@base_router.get("/")
async def read_root():
    return {"status": "API is running..."}