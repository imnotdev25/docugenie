from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import validates
from app.utils.file_utils import clean_text


# type alias for chat history
ChatHistory = List[Dict[str, str]]

ChatHistoryInit = [
    {
        "user_input": "Hello! There!!!",
        "assistant_response": "Hi there! I'm docugenie, your document assistant. How can I help you today?"
    }
]

class Users(SQLModel, table=True):
    __tablename__ = "users"

    user_id: UUID = Field(default_factory=uuid4, primary_key=True)
    doc_uuid: UUID = Field(default_factory=uuid4, unique=True)
    doc_metadata: Dict = Field(default={}, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    chat_history: List[Dict[str, str]] = Field(
        default=ChatHistoryInit,
        sa_column=Column(JSONB))


class DocumentSection(SQLModel, table=True):
    __tablename__ = "document_sections"

    id: Optional[int] = Field(default=None, primary_key=True)
    doc_uuid: UUID = Field(foreign_key="users.doc_uuid")
    content: str
    embedding: List[Any] = Field(sa_column=Column(Vector(1536)))
    section_number: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validates('content')
    def validate_content(self, key, value):
        if value is not None:
            return clean_text(value)
        return value
