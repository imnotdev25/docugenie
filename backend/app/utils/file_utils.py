import os
import re
from typing import Optional
from fastapi import UploadFile
import aiofiles
import logfire

from app.models.file import File, FileType
from app.config import settings

async def save_uploaded_file(file: UploadFile, doc_uuid: str) -> str:
    """
    Save uploaded file to local storage.

    Args:
        file: The uploaded file
        doc_uuid: The document UUID

    Returns:
        str: The path where the file was saved
    """
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        # Generate file path
        file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_uuid}_{file.filename}")

        # Save file asynchronously
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        return file_path

    except Exception as e:
        logfire.error(f"Error saving file: {str(e)}")
        raise

async def upload_file_s3(file: UploadFile, path: str) -> bool:
    """
    Upload file to S3 (placeholder for future implementation).

    Args:
        file: The file to upload
        path: The S3 path

    Returns:
        bool: True if successful
    """
    # TODO: Implement S3 upload
    pass

async def download_file_s3(file: str, path: str) -> bool:
    """
    Download file from S3 (placeholder for future implementation).

    Args:
        file: The file to download
        path: The S3 path

    Returns:
        bool: True if successful
    """
    # TODO: Implement S3 download
    pass

def is_valid_file(filename: str) -> bool:
    """
    Check if file type is supported.

    Args:
        filename: Name of the file

    Returns:
        bool: True if file type is supported
    """
    file = File(name=filename)
    return file.type is not None

def get_file_type(filename: str) -> Optional[FileType]:
    """
    Get the file type from filename.

    Args:
        filename: Name of the file

    Returns:
        FileType: The type of the file or None if not supported
    """
    file = File(name=filename)
    return file.type

def generate_file_path(filename: str, doc_uuid: str) -> str:
    """
    Generate file path for uploaded file.

    Args:
        filename: Original filename
        doc_uuid: Document UUID

    Returns:
        str: Generated file path
    """
    return os.path.join(settings.UPLOAD_DIR, f"{doc_uuid}_{filename}")

def cleanup_file(file_path: str) -> None:
    """
    Clean up uploaded file after processing.

    Args:
        file_path: Path to the file to clean up
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logfire.error(f"Error cleaning up file {file_path}: {str(e)}")
        raise


def clean_text(text: str) -> str:
    """
    Clean text by removing null bytes and other problematic characters
    """
    if not isinstance(text, str):
        return ""

    # Remove null bytes and other problematic characters
    cleaned = text.encode('utf-8', errors='ignore').decode('utf-8')

    # Replace various types of whitespace and control characters
    cleaned = re.sub(r'[\x00-\x1F\x7F-\x9F]', ' ', cleaned)

    # Replace multiple spaces with single space
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # Replace problematic unicode characters
    cleaned = re.sub(r'[\u2028\u2029\uFEFF\uFFFD]', ' ', cleaned)

    # Remove zero-width spaces and other invisible separators
    cleaned = re.sub(r'[\u200B-\u200D\uFEFF]', '', cleaned)

    # Normalize quotes and dashes
    cleaned = cleaned.replace('"', '"').replace('"', '"')
    cleaned = cleaned.replace(''', "'").replace(''', "'")
    cleaned = cleaned.replace('–', '-').replace('—', '-')

    # Strip whitespace
    cleaned = cleaned.strip()

    return cleaned
