from langchain_openai import ChatOpenAI

from app.config import settings
from app.models.users import ChatHistory


def summarize_doc(document_content: str, query: str, chat_history: ChatHistory) -> str:
    chat = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_MODEL)
    history_context = "\n".join(
        f"User: {history['user_input']}\nBot: {history['response']}" for history in chat_history)
    complete_prompt = f"""
    Here is the document context:
    {document_content}

    Based on the following conversation history:
    {history_context}

    Please provide an answer to the following query: {query}"""
    response = chat.call_as_chain(instruction=complete_prompt)
    return response
