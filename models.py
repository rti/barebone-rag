import ollama
import enum
from typing import List

_client_embedding = None
_client_chat = None

embeddingsModel = "nomic-embed-text"

# TODO: adjust EmbeddingPrefix when enabling other models
# embeddingsModel = "all-minilm"
# embeddingsModel = "mxbai-embed-large"
# embeddingsModel = "znbang/bge:large-en-v1.5-f16"


# Note: prefixes specific to nomic-embed-text
class EmbeddingPrefix(enum.Enum):
    DOCUMENT = "search_document: "
    QUERY = "search_query: "
    NONE = ""


chatModel = "mistral:v0.2"
# chatModel = "zephyr:7b-beta"
# chatModel = "openchat:7b-v3.5-0106"
# chatModel = "stablelm2:1.6b"
# chatModel = "command-r:v0.1"
# chatModel = "phi3:mini"
# chatModel = "llama3:8b"
# chatModel = "gemma:7b-v1.1"
# chatModel = "gemma:2b-v1.1"
# chatModel = "qwen:0.5b"


def get_connection_embedding():
    global _client_embedding
    if not _client_embedding:
        _client_embedding = ollama.Client(host="ollama-embedding:11434")
        _client_embedding.pull(model=embeddingsModel)
    return _client_embedding


def get_connection_chat():
    global _client_chat
    if not _client_chat:
        _client_chat = ollama.Client(host="ollama-chat:11434")
        _client_chat.pull(model=chatModel)
    return _client_chat


def embedding(input: str, prefix=EmbeddingPrefix.NONE) -> list[float]:
    client = get_connection_embedding()
    prompt = prefix.value + input
    res = client.embeddings(model=embeddingsModel, prompt=prompt)
    return res["embedding"]  # type: ignore # ollama gets something wrong here


def embedding_string(input: str, prefix=EmbeddingPrefix.NONE) -> str:
    e = embedding(input, prefix)
    return "[" + ", ".join([str(num) for num in e]) + "]"


def embedding_length() -> int:
    return len(embedding("Hello world"))


def chat(
    input: str, system: List[str] = ["You are a helpful assistant."], stream=False
):
    client = get_connection_chat()

    system_messages = [ollama.Message({"role": "system", "content": s}) for s in system]
    user_message = [ollama.Message({"role": "user", "content": input})]

    res = client.chat(
        model=chatModel,
        messages=system_messages + user_message,
        options={"temperature": 0.0},
        stream=stream,
    )

    if stream:
        return res
    return res["message"]["content"]  # type: ignore # ollama gets something wrong here
