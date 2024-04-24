import models
import postgres

chunks = postgres.get_random_chunks(1)

system = """\
Your task is to write a factoid question.
Your question should be answerable with a specific, concise piece of factual information from the context.
Your question should be formulated in the same style as questions users could ask in a search engine.
This means that your question MUST NOT mention something like "according to the passage" or "context".
"""

for chunk in chunks:
    prompt = f"""
Here is the context:
{chunk.title} {chunk.description if chunk.description is not None else ''}\n
... {chunk.text}\n
End of context.

Create one very short factoid question about the context above. Do not provide any justification, only the queestion.
"""

    # print("Prompt:\n\n" + prompt + "\n\n\n")
    print("\n*******************************************************************************\n")
    print(prompt)
    print("\n*******************************************************************************\n")
    print(models.chat(prompt, system))
    print("\n*******************************************************************************")
    print("*******************************************************************************")
    print("*******************************************************************************")
    print()
