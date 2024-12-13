from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    doc_uuid: UUID
    query: str
    limit: Optional[int] = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    section_number: int
    content: str
    doc_uuid: UUID

    def model_dump(self):
        return {
            "section_number": self.section_number,
            "content": self.content,
            "doc_uuid": str(self.doc_uuid)
        }


class QueryResponse(BaseModel):
    results: List[SearchResult]
    message: str

class QueryResponseWithGPT(QueryResponse):
    gpt_response: str

