import os
import uuid

from fastapi import APIRouter, UploadFile, HTTPException

from app.utils.file_utils import save_uploaded_file, is_valid_file
from app.models.file import FileType
from app.services.ingest import read_content, read_url_content
from app.services.chunking import process_file
from app.services.text_embedding import text_to_tokens
from app.services.vector_db_crud import save_embeddings
from app.services.db_crud import save_user
from app.utils.file_utils import file_uuid
from app.logger import logger


du_upload_router = APIRouter()


@du_upload_router.post("/upload/file")
def upload_file(file: UploadFile):
    # max_size 4MB
    if file.size > 4 * 1024 * 1024:
        logger.error(f"File size is too large: {file.size}")
        raise HTTPException(status_code=400, detail="File size is too large.")
    if not is_valid_file(file.filename):
        logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type.")
    doc_uuid = file_uuid()
    save_uploaded_file(file, os.path.join("uploads", file.filename))
    file_type = FileType[file.filename.split(".")[-1].lower()]
    content = read_content(os.path.join("uploads", file.filename), file_type)
    chunks = process_file(content, 512)
    embeddings = text_to_tokens(chunks)
    save_embeddings(str(uuid.uuid4()), {"filename": file.filename, "type": file_type.value}, embeddings, doc_uuid)
    user_id = save_user(user_data={"doc_uuid": doc_uuid, "doc_metadata": {"filename": file.filename, "type": file_type.value}})
    logger.info(f"Uploaded file: {file.filename} with UUID: {doc_uuid} and User ID: {user_id}")
    return {"uuid": doc_uuid}


@du_upload_router.post("/upload/url")
def upload_url(url: str):
    try:
        content = read_url_content(url)
        doc_uuid = file_uuid()
        embeddings = process_file(content, 512)
        save_embeddings(str(uuid.uuid4()), {"url": url}, embeddings, doc_uuid)
        user_id = save_user(user_data={"doc_uuid": doc_uuid, "doc_metadata": {"url": url}})
        logger.info(f"Uploaded URL: {url} with UUID: {doc_uuid} and User ID: {user_id}")
        return {"uuid": doc_uuid}
    except Exception as e:
        logger.error(f"Error uploading URL: {e}")
        raise HTTPException(status_code=400, detail="Error uploading URL") from e
