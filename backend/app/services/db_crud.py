from app.databases.db import get_session
from app.models.users import Users, ChatHistory
from app.logger import logger


def save_user(user_data: dict):
    with next(get_session()) as session:
        try:
            new_user = Users(
                doc_uuid=user_data['doc_uuid'],
                doc_metadata=user_data['doc_metadata']
            )
            session.add(new_user)
            session.commit()
            return new_user.user_id
        except Exception as err:
            logger.error(f"Error saving user: {err}")
            raise Exception(f"Error saving user: {err}") from err

def save_chat_history(doc_id: str, chat_history: ChatHistory | dict):
    with next(get_session()) as session:
        try:
            user = session.get(Users, doc_id)
            user.chat_history.append(chat_history)
            session.add(user)
            session.commit()
            return user.id
        except Exception as err:
            logger.error(f"Error saving chat history: {err}")
            raise Exception(f"Error saving chat history: {err}") from err

def get_chat_history(doc_id: str) -> ChatHistory:
    with next(get_session()) as session:
        try:
            user = session.get(Users, doc_id)
            return user.chat_history
        except Exception as err:
            logger.error(f"Error getting chat history: {err}")
            raise Exception(f"Error getting chat history: {err}") from err