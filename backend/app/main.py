
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.base import base_router
from app.api.docu_upload import upload_router
from app.api.docu_query import query_router
from app.config import settings
from app.lifetime import shutdown
from app.lifetime import startup
import logfire


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI backend for RAG-based document querying",
    version="0.1.0",
)

# Logfire
logfire.configure(
    token=settings.LOGFIRE_TOKEN,
    service_name=settings.PROJECT_NAME,
)
logfire.instrument_fastapi(app)


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
app.include_router(upload_router, prefix=settings.API_PREFIX, tags=["upload"])
app.include_router(query_router, prefix=settings.API_PREFIX, tags=["query"])
