import models
import postgres

chunks = postgres.get_random_chunks(1)

system = """\
Your task is to write factoid questions and answers given a context.
Your questions should be answerable with a specific, concise piece of factual information from the context.
Your questions should be formulated in the same style as questions users could ask in a search engine.
This means that your questions MUST NOT mention something like "according to the passage" or "context".
"""

for chunk in chunks:
    prompt = """\
Provide your questions and answers in the follwing json structure:

{
    "chunk_id": "<chunk_id>",
    "question": "your question 1",
    "answer": "your answer to question 1",
}

""" + f"""
Now here is the context.
Chunk ID: {chunk.id}
Context:
{chunk.text}\n

Create one factoid question with answer about the context above in a json structure.
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
