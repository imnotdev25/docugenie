import re

import tiktoken


def remove_special_characters(content: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\s.]', '', content)


def remove_extra_whitespace(content: str) -> str:
    return re.sub(r'\s+', ' ', content).strip()


def preprocess_content(content: str) -> str:
    # Chain of preprocessing functions
    content = remove_special_characters(content)
    content = remove_extra_whitespace(content)
    content.lower()
    return content


def split_based_on_tokens(content: str, max_tokens: int = 512, overlap_tokens: int = 100) -> list:
    encoder = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoder.encode(content)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk = tokens[start:end]
        chunks.append(encoder.decode(chunk))
        start += max_tokens - overlap_tokens

    return chunks


def process_file(content: str, max_tokens: int):
    # Preprocess content
    preprocessed_content = preprocess_content(content)

    # Split into chunks based on token length
    content_chunks = split_based_on_tokens(preprocessed_content, max_tokens)

    return content_chunks
