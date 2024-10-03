from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Tokenize input text
print(tokenizer.encode("hello"))

print(tokenizer.decode([101, 7592, 1010, 2026, 3899, 2003, 10140, 102]))