from uuid import uuid4, UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Column
from typing import List, Dict, Optional

# type alias for chat history
ChatHistory = List[Dict[str, str]]

ChatHistoryInit = [
    {
        "user_input": "Hello!",
        "response": "Hi there! I'm docugenie, your document assistant. How can I help you today?"
    }
]

class Users(SQLModel, table=True):
    user_id: UUID = Field(default=uuid4(), primary_key=True)
    doc_uuid: UUID
    doc_metadata: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    chat_history: ChatHistory = Field(default=ChatHistoryInit, sa_column=Column(JSONB))
