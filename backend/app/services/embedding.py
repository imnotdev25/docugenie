from transformers import AutoTokenizer, AutoModel


# Tokenize input text

def tokenize_input_text(text: str | list) -> list:
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    return tokenizer.encode(text)
