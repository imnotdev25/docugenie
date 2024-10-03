import re
from pathlib import Path

import tiktoken

from backend.app.models.file import File


def remove_special_characters(content: str) -> str:
    # Remove characters except for whitespace, commas, and dots
    return re.sub(r'[^a-zA-Z0-9\s.,]', '', content)


def remove_extra_whitespace(content: str) -> str:
    # Replace multiple spaces/newlines with a single space
    return re.sub(r'\s+', ' ', content).strip()


def preprocess_content(content: str) -> str:
    # Chain of preprocessing functions
    content = remove_special_characters(content)
    content = remove_extra_whitespace(content)
    content.lower()
    return content


def split_based_on_tokens(content: str, max_tokens: int = 512) -> list:
    encoder = tiktoken.get_encoding("cl100k_bas")  # Adjust as needed
    tokens = encoder.encode(content)

    split_content = []
    for i in range(0, len(tokens), max_tokens):
        sub_tokens = tokens[i:i + max_tokens]
        sub_text = encoder.decode(sub_tokens)
        split_content.append(sub_text)

    return split_content


# Example usage:
def process_file(file_path: str, max_tokens: int):
    file_instance = File(path=Path(file_path))
    raw_content = file_instance.read_content()

    # Preprocess content
    preprocessed_content = preprocess_content(raw_content)

    # Split into chunks based on token length
    content_chunks = split_based_on_tokens(preprocessed_content, max_tokens)

    return content_chunks
