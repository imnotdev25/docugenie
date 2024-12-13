from typing import List
from uuid import UUID

import logfire
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.databases.db import get_session
from app.llms.openai_llm import GPTService
from app.models.database import ChatHistory
from app.models.database import DocumentSection
from app.models.query import (
    QueryRequest,
    SearchResult
)
from app.models.query import QueryResponseWithGPT
from app.services.query_service import semantic_search
from app.services.text_embedding import create_embedding
from app.services.user_service import get_user_by_doc_uuid
from app.services.user_service import update_chat_history

query_router = APIRouter()
gpt_service = GPTService()


@query_router.post("/query", response_model=QueryResponseWithGPT)
async def query_document(
        query_request: QueryRequest,
        session: AsyncSession = Depends(get_session)
):
    """
    Query a document using semantic search and generate GPT response
    """
    try:
        # Get user and chat history
        user = await get_user_by_doc_uuid(session, query_request.doc_uuid)

        # Create embedding for the query
        query_embedding = await create_embedding(query_request.query)

        # Perform semantic search
        search_results = await semantic_search(
            query_embedding=query_embedding,
            doc_uuid=query_request.doc_uuid,
            session=session,
            limit=query_request.limit or settings.DEFAULT_SEARCH_LIMIT
        )
        logfire.info(f"Found {len(search_results)} relevant sections")


        if not search_results:
            return QueryResponseWithGPT(
                results=[],
                message="No relevant results found",
                gpt_response="No relevant context found to answer the query."
            )

        # Generate GPT response using chat history from user
        gpt_response = await gpt_service.generate_response(
            document_sections=search_results,
            query=query_request.query,
            chat_history=user.chat_history
        )
        logfire.info(f"Generated GPT response {gpt_response}")

        # Update chat history

        resp = await update_chat_history(
            session=session,
            doc_uuid=query_request.doc_uuid,
            user_input=query_request.query,
            response=gpt_response
        )
        logfire.info(f"Updated chat history for user {resp}")

        return QueryResponseWithGPT(
            results=search_results,
            message=f"Found {len(search_results)} relevant sections",
            gpt_response=gpt_response
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@query_router.get("/documents/{doc_uuid}/sections", response_model=List[SearchResult])
async def get_document_sections(
        doc_uuid: UUID,
        session: AsyncSession = Depends(get_session)
):
    """
    Get all sections of a specific document
    """
    try:
        stmt = select(DocumentSection).where(
            DocumentSection.doc_uuid == doc_uuid
        ).order_by(DocumentSection.section_number)

        result = await session.execute(stmt)
        sections = result.scalars().all()

        if not sections:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )

        return [
            SearchResult(
                content=section.content,
                section_number=section.section_number,
                doc_uuid=section.doc_uuid
            )
            for section in sections
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document sections: {str(e)}"
        )


@query_router.get("/documents/{doc_uuid}/chat-history", response_model=ChatHistory)
async def get_chat_history(
    doc_uuid: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get chat history for a document"""
    try:
        user = await get_user_by_doc_uuid(session, doc_uuid)
        return user.chat_history
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat history: {str(e)}"
        )

@query_router.delete("/documents/{doc_uuid}/chat-history")
async def clear_chat_history(
    doc_uuid: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Clear chat history for a document"""
    try:
        user = await get_user_by_doc_uuid(session, doc_uuid)
        user.chat_history = user.chat_history[:1]  # Keep only the initial greeting
        await session.commit()
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing chat history: {str(e)}"
        )

