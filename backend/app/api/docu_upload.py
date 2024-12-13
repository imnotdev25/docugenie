from uuid import UUID, uuid4

import logfire
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.db import get_session
from app.models.api import UploadResponse
from app.models.database import DocumentSection
from app.services.document_service import read_content, read_url_content
from app.services.text_embedding import split_into_chunks, create_embedding
from app.services.user_service import get_user_by_doc_uuid, create_user
from app.utils.file_utils import is_valid_file, get_file_type, save_uploaded_file, clean_text

upload_router = APIRouter()


@upload_router.post("/upload/file", response_model=UploadResponse)
async def upload_file(
        file: UploadFile,
        session: AsyncSession = Depends(get_session)
):
    """Upload and process a document file"""
    try:
        # Validate file type and size
        if not is_valid_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        if file.size > 4 * 1024 * 1024:
            logfire.error(f"File size is too large: {file.size}")
            raise HTTPException(status_code=400, detail="File size is too large.")

        doc_uuid = uuid4()

        # Save file
        file_path = await save_uploaded_file(file, doc_uuid)
        file_type = get_file_type(file.filename)
        if not file_path:
            raise HTTPException(
                status_code=500,
                detail="Error saving file"
            )
        text_content = read_content(file_path, file_type)
        if not text_content:
            raise HTTPException(
                status_code=400,
                detail="Could not read file content"
            )

        # Prepare metadata
        metadata = {
            "filename": file.filename,
            "file_path": file_path,
            "size": len(text_content),
        }

        # Create user first
        await create_user(session, doc_uuid, metadata)

        # Split into chunks
        chunks = await split_into_chunks(text_content)
        #
        # # Process chunks and create embeddings
        for i, chunk in enumerate(chunks):
            embedding = await create_embedding(chunk)

            doc_section = DocumentSection(
                doc_uuid=doc_uuid,
                content=clean_text(chunk),
                embedding=embedding,
                section_number=i
            )
            session.add(doc_section)

        await session.commit()

        return UploadResponse(
            doc_uuid=doc_uuid,
            message="Document processed successfully"
        )

    except Exception as e:
        await session.rollback()
        logfire.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing upload"
        )

@upload_router.post("/upload/url", response_model=UploadResponse)
async def upload_url(
        url: str,
        session: AsyncSession = Depends(get_session)
):
    """Upload and process a URL"""
    try:
        doc_uuid = uuid4()

        # Read content from URL
        text_content = read_url_content(url)
        if not text_content:
            raise HTTPException(
                status_code=400,
                detail="Could not read URL content"
            )

        # Prepare metadata
        metadata = {
            "url": url,
            "size": len(text_content),
        }

        # Create user first
        await create_user(session, doc_uuid, metadata)

        # Split into chunks
        chunks = await split_into_chunks(text_content)

        # Process chunks and create embeddings
        for i, chunk in enumerate(chunks):
            embedding = await create_embedding(chunk)

            doc_section = DocumentSection(
                doc_uuid=doc_uuid,
                content=clean_text(chunk),
                embedding=embedding,
                section_number=i
            )
            session.add(doc_section)

        await session.commit()

        return UploadResponse(
            doc_uuid=doc_uuid,
            message="URL processed successfully"
        )

    except Exception as e:
        await session.rollback()
        logfire.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing URL"
        )


@upload_router.get("/documents/{doc_uuid}")
async def check_document(
        doc_uuid: UUID,
        session: AsyncSession = Depends(get_session)
):
    """Check if document exists and return its metadata"""
    try:
        user = await get_user_by_doc_uuid(session, doc_uuid)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return {
            "doc_uuid": user.doc_uuid,
            "metadata": user.doc_metadata,
            "created_at": user.created_at
        }

    except HTTPException:
        raise
    except Exception as e:
        logfire.error(f"Error checking document: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error checking document"
        )
