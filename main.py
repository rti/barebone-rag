import ollama

from collections.abc import Iterator

model = "qwen:0.5b"

client = ollama.Client(host="localhost:51434")

# client.pull(model)

stream = client.chat(
    model=model,
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

if not isinstance(stream, Iterator):
    raise Exception

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)
