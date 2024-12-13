from uuid import UUID

import logfire
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import ChatHistory
from app.models.database import Users


async def get_user_by_doc_uuid(session: AsyncSession, doc_uuid: UUID) -> Users | None:
    """Check if user exists with given doc_uuid"""
    try:
        query = select(Users).where(Users.doc_uuid == doc_uuid)
        result = await session.execute(query)
        return result.scalar()
    except Exception as e:
        logfire.error(f"Error checking user existence: {str(e)}")
        raise

async def create_user(
    session: AsyncSession,
    doc_uuid: UUID,
    metadata: dict
) -> Users:
    """Create new user with document metadata"""
    try:
        user = Users(doc_uuid=doc_uuid, doc_metadata=metadata)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except Exception as e:
        await session.rollback()
        logfire.error(f"Error creating user: {str(e)}")
        raise


async def update_chat_history(
        session: AsyncSession,
        doc_uuid: UUID,
        user_input: str,
        response: str
) -> Users:
    """Update chat history for the user"""
    try:
        # Get or create user
        user = await get_user_by_doc_uuid(session, doc_uuid)

        # Create new chat entry
        new_chat_entry = {
            "user_input": user_input,
            "response": response
        }

        # Update chat history
        user.chat_history.append(new_chat_entry)

        # Mark as modified
        session.add(user)

        # Commit changes
        await session.commit()

        # Refresh user instance
        await session.refresh(user)

        logfire.info(f"Chat history updated for doc_uuid: {doc_uuid} with new entry: {user.chat_history}")
        return user

    except Exception as e:
        logfire.error(f"Error updating chat history: {str(e)}")
        await session.rollback()
        raise Exception(f"Error updating chat history: {str(e)}")

