import ollama

_client = None

embeddingsModel = "all-minilm"  # or: mxbai-embed-large
# chatModel = "qwen:0.5b"
# chatModel = "gemma:7b"
chatModel = "mistral:v0.2"


def get_connection():
    global _client
    if not _client:
        _client = ollama.Client(host="ollama:11434")
        _client.pull(model=embeddingsModel)
        _client.pull(model=chatModel)
    return _client


def embedding(input: str) -> list[float]:
    client = get_connection()
    res = client.embeddings(model=embeddingsModel, prompt=input)
    return res["embedding"]  # type: ignore # ollama gets something wrong here


def embeddingString(input: str) -> str:
    e = embedding(input)
    return "[" + ", ".join([str(num) for num in e]) + "]"


def embeddingLength() -> int:
    return len(embedding("Hello world"))


def chat(input: str):
    client = get_connection()
    res = client.chat(
        model=chatModel,
        messages=[{"role": "user", "content": input}],
        stream=False,
    )
    return res["message"]["content"] # type: ignore
