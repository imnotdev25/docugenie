import uuid
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Column, String
from sqlmodel.sql.sqltypes import Any


class TextEmbedding(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    doc_uuid: Optional[str] = Field(sa_column=Column(String))
    doc_metadata: Optional[dict] = Field(sa_column=Column(JSONB))
    embedding: Any = Field(sa_column=Column(Vector()))
