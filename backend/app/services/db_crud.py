from app.databases.db import get_session
from app.models.users import Users
from app.logger import logger


def save_user(user_data: Users):
    with next(get_session()) as session:
        try:
            new_user = Users(
                short_id=user_data.short_id,
                doc_uuid=user_data.doc_uuid,
                doc_metadata=user_data.doc_metadata,
                chat_history=user_data.chat_history
            )
            session.add(new_user)
            session.commit()
            return new_user.id
        except Exception as err:
            logger.error(f"Error saving user: {err}")
            raise Exception(f"Error saving user: {err}") from err

def save_chat_history(doc_id: int, chat_history: dict):
    with next(get_session()) as session:
        try:
            user = session.get(Users, doc_id)
            user.chat_history = chat_history
            session.add(user)
            session.commit()
            return user.id
        except Exception as err:
            logger.error(f"Error saving chat history: {err}")
            raise Exception(f"Error saving chat history: {err}") from err

def get_chat_history(doc_id: int) -> dict:
    with next(get_session()) as session:
        try:
            user = session.get(Users, doc_id)
            return user.chat_history
        except Exception as err:
            logger.error(f"Error getting chat history: {err}")
            raise Exception(f"Error getting chat history: {err}") from err