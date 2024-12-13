from fastapi import FastAPI

from app.databases.db import init_db, close_db


def startup(app: FastAPI):
    async def _startup():
        await init_db()

    return _startup


def shutdown(app: FastAPI):
    async def _shutdown():
        await close_db()

    return _shutdown

