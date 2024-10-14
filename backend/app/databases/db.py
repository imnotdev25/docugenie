from sqlmodel import SQLModel, create_engine, Session

from app.config import settings

PGVECTOR_URI = f"postgresql+psycopg2://{settings.POSTGRES_URI.split('://')[1]}"

engine = create_engine(PGVECTOR_URI, pool_size=16, max_overflow=32, pool_recycle=900, pool_pre_ping=True)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.create_all(engine)


def close_db():
    engine.dispose()
