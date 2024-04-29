import ollama
import enum

_client = None

# embeddingsModel = "all-minilm" # 384 dimensional embeddings model - apache-2.0
# embeddingsModel = "mxbai-embed-large" # 1024 dimensional embeddings model - apache-2.0
# embeddingsModel = "znbang/bge:large-en-v1.5-f16" # 1024 dimensoinal embeddings model - MIT

embeddingsModel = "nomic-embed-text"  # 768 dimensional embeddings model - apache-2.0


class EmbeddingPrefix(enum.Enum):
    DOCUMENT = "search_document: "
    QUERY = "search_query: "
    NONE = ""


# chatModel = "mistral:v0.2"
chatModel = "zephyr:7b-beta"
# chatModel = "openchat:7b-v3.5-0106"
# chatModel = "qwen:0.5b"
# chatModel = "gemma:7b-v1.1"
# chatModel = "gemma:2b-v1.1"
# chatModel = "stablelm2:1.6b"
# chatModel = "command-r:v0.1"


def get_connection():
    global _client
    if not _client:
        _client = ollama.Client(host="ollama:11434")
        _client.pull(model=embeddingsModel)
        _client.pull(model=chatModel)
    return _client


def embedding(input: str, prefix=EmbeddingPrefix.NONE) -> list[float]:
    client = get_connection()
    prompt = prefix.value + input
    res = client.embeddings(model=embeddingsModel, prompt=prompt)
    return res["embedding"]  # type: ignore # ollama gets something wrong here


def embeddingString(input: str, prefix=EmbeddingPrefix.NONE) -> str:
    e = embedding(input, prefix)
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
