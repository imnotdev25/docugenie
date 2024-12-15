from openai import AsyncAzureOpenAI
from typing import List

import logfire

from app.config import settings
from app.models.database import ChatHistory

class GPTService:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_key=settings.AZURE_API_KEY,
            api_version=settings.AZURE_API_VERSION,
            azure_endpoint=settings.AZURE_ENDPOINT
        )
        # Init with AsyncOpenai for openai API

    async def generate_response(
            self,
            document_sections: List[dict],
            query: str,
            chat_history: ChatHistory | None
    ) -> str:
        # Combine document sections into context
        document_context = "\n\n".join(
            f"Section {section['section_number']}:\n{section['content']}"
            for section in document_sections
        )

        # Format chat history if available
        history_context = ""
        if chat_history:
            history_context = "\n".join(
                f"User: {history['user_input']}: \nAssistant: {history['assistant_response']}"
                for history in chat_history
            )

        # Create the complete prompt
        system_prompt = """You are a helpful assistant that answers questions based on the provided document context. 
        Always base your answers on the given context and be precise and concise."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""
            Context:
            {document_context}

            Previous conversation:
            {history_context}

            Question: {query}

            Please provide a clear and concise answer based on the context provided.
            """}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logfire.error(f"Error generating GPT response: {str(e)}")
            raise Exception(f"Error generating GPT response: {str(e)}")