from fastapi import FastAPI


# from app.database.db import init_db, shutdown_db


def startup(app: FastAPI):
    async def _startup():
        pass  # await init_db()

    return _startup


def shutdown(app: FastAPI):
    async def _shutdown():
        pass
        # await shutdown_db()

    return _shutdown
