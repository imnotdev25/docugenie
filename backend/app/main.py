from sys import prefix

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.base import base_router
from app.api.docu_upload import du_upload_router
from app.api.docu_query import docu_query_router
from app.config import settings
from app.lifetime import shutdown
from app.lifetime import startup



app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI backend for RAG-based document querying",
    version="0.1.0",
)


app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", shutdown(app))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    expose_headers=["*"],
)

# Register the API router
app.include_router(base_router, prefix=settings.API_PREFIX)
app.include_router(du_upload_router, prefix=settings.API_PREFIX)
app.include_router(docu_query_router, prefix=settings.API_PREFIX)
