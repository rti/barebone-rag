import models
import postgres
import sys

def print2(*args): print(*args, file=sys.stderr)


chunks = postgres.get_random_chunks(1)

system = """\
Your are a helpful assistent supporting the creation of a question answer system.
"""

for chunk in chunks:

    prompt = f"""\
Your task is to write a factoid question.
Your question should be answerable with a specific, concise piece of factual information from the context.
Your question should be formulated in the same style as questions users could ask in a search engine.
This means that your question MUST NOT mention something like "according to the passage" or "context".

Here is the context:
{chunk.title} {chunk.description if chunk.description is not None else ''}\n
... {chunk.text}\n
End of context.

Create one very short factoid question about the context above. Do not provide any justification, only the queestion.
"""

    response = models.chat(prompt, system)
    print2("\n*******************************************************************************\n")
    print2(prompt)
    print2("\n*******************************************************************************\n")
    print2(response)
    print2("\n*******************************************************************************\n")
    print(f"""{{ "question": "{response}", "chunk-id": "{chunk.id}" }}""")
    print2("\n*******************************************************************************")
    print2("*******************************************************************************")
    print2("*******************************************************************************")
    print2()
