import ollama

_client = None

embeddingsModel = "all-minilm" # or: mxbai-embed-large

def get_connection():
    global _client
    if not _client:
        _client = ollama.Client(host="ollama:11434")
        _client.pull(model=embeddingsModel)
    return _client

def embedding(input):
    client = get_connection()
    res = client.embeddings(model=embeddingsModel, prompt=input)
    return res["embedding"] # type: ignore # ollama gets something wrong here

def embeddingLength():
    return len(embedding("Hello world"))

