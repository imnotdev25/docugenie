from typing import List
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.query import (
    SearchResult
)


async def semantic_search(
        query_embedding: List[float],
        doc_uuid: UUID,
        session: AsyncSession,
        limit: int = 8
) -> List[dict]:
    """
    Perform semantic search using vector similarity within a specific document
    Returns section_number, content, and doc_uuid ordered by vector distance
    """
    # Convert the embedding list to a string representation
    embedding_str = f"[{','.join(str(x) for x in query_embedding)}]"

    query = f"""
    SELECT section_number, content, doc_uuid
    FROM document_sections 
    WHERE doc_uuid = :doc_uuid
    ORDER BY embedding <-> '{embedding_str}'::vector
    LIMIT :limit
    """

    try:
        result = await session.execute(
            text(query),
            {
                "doc_uuid": doc_uuid,
                "limit": limit
            }
        )
        matches = result.all()

        return [
            SearchResult(
                section_number=match.section_number,
                content=match.content,
                doc_uuid=match.doc_uuid
            ).model_dump()
            for match in matches
        ]
    except Exception as e:
        print(f"Error during semantic search: {e}")
        raise  # This will help us see the full error
