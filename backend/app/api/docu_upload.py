import os
import uuid

from fastapi import APIRouter, UploadFile, HTTPException
from backend.app.utils.file_utils import save_uploaded_file, is_valid_file


du_upload_router = APIRouter()


@du_upload_router.post("/upload/file")
def upload_file(file: UploadFile):
    # max_size 4MB
    if file.size > 4 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size is too large.")
    if not is_valid_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type.")
    save_uploaded_file(file, os.path.join("uploads", file.filename))

    return {"uuid": str(uuid.uuid4()), "filename": file.filename}


@du_upload_router.post("/upload/url")
def upload_url(url: str):
    pass