from uuid import uuid4

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Column
from typing import List, Dict

# type alias for chat history
ChatHistory = List[Dict[str, str]]

ChatHistoryInit = [
    {
        "user_input": "Hello!",
        "response": "Hi there! I'm docugenie, your document assistant. How can I help you today?"
    }
]

class Users(SQLModel, table=True):
    id: int = Field(default=uuid4(), primary_key=True)
    short_id: str
    doc_uuid: str
    doc_metadata: dict
    chat_history: ChatHistory = Field(default=ChatHistoryInit, sa_column=Column(JSONB))
