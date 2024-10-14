import tiktoken
from app.logger import logger


def text_to_tokens(text: str | list, encoder: str = "gpt-4o") -> list:
    encoder = tiktoken.encoding_for_model(encoder)
    if isinstance(text, str):
        return encoder.encode(text)
    elif isinstance(text, list):
        return [encoder.encode(t) for t in text]
    else:
        logger.error("Input text must be a string or a list of strings.")
        raise ValueError("Input text must be a string or a list of strings.")


def tokens_to_text(tokens: list, encoder: str = "gpt-4o") -> str:
    encoder = tiktoken.encoding_for_model(encoder)
    content = encoder.decode(tokens)
    return content