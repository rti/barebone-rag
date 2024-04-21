import ollama

_client = None

embeddingsModel = "all-minilm"  # or: mxbai-embed-large
# chatModel = "mistral:v0.2"
chatModel = "zephyr:7b"
# chatModel = "openchat:7b-v3.5-0106"
# chatModel = "qwen:0.5b"
# chatModel = "gemma:7b"
# chatModel = "command-r"


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


def chat(input: str, system: str = "You are a helpful assistant."):
    client = get_connection()
    res = client.chat(
        model=chatModel,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": input},
        ],
        stream=False,
    )
    return res["message"]["content"]  # type: ignore
