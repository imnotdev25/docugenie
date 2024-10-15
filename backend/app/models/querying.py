from pydantic import BaseModel


class QueryRequest(BaseModel):
    doc_uuid: str
    query: str

class QueryResponse(BaseModel):
    response: str