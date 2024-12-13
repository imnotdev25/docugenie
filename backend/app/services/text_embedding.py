from typing import List

import logfire
import tiktoken
from openai import AsyncAzureOpenAI

from app.config import settings


def get_tokenizer():
    """Get the cl100k_base tokenizer (used by text-embedding-3-small)"""
    return tiktoken.encoding_for_model("gpt-4o")


async def split_into_chunks(
        text: str,
        chunk_size: int = 1536,
        overlap: int = 50
) -> List[str]:
    """Split text into chunks using tiktoken"""
    try:
        enc = get_tokenizer()
        tokens = enc.encode(text)
        chunks = []

        i = 0
        while i < len(tokens):
            # Get chunk of tokens
            chunk_end = min(i + chunk_size, len(tokens))
            chunk_tokens = tokens[i:chunk_end]

            # Decode chunk back to text
            chunk_text = enc.decode(chunk_tokens)
            chunks.append(chunk_text)

            # Move to next chunk with overlap
            i += (chunk_size - overlap)

        return chunks
    except Exception as e:
        logfire.error(f"Error splitting text: {str(e)}")
        raise



async def create_embedding(text: str) -> List[float]:
    """Create embedding using text-embedding-3-small"""
    try:
        client = AsyncAzureOpenAI(
            azure_endpoint=settings.AZURE_ENDPOINT,
            api_key=settings.AZURE_API_KEY,
            api_version=settings.AZURE_API_VERSION
        )

        response = await client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )

        return response.data[0].embedding
    except Exception as e:
        logfire.error(f"Error creating embedding: {str(e)}")
        raise

