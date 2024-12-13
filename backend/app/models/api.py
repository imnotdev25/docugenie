from uuid import UUID

from pydantic import BaseModel


class UploadResponse(BaseModel):
    doc_uuid: UUID
    message: str



