import models
import postgres

pages = postgres.get_random_pages(1)

system = """\
Your task is to write factoid questions and answers given a context.
Your questions should be answerable with a specific, concise piece of factual information from the context.
Your questions should be formulated in the same style as questions users could ask in a search engine.
This means that your questions MUST NOT mention something like "according to the passage" or "context".
"""

for page in pages:
    prompt = """\
Provide your questions and answers in the follwing json structure:

{
    "page_id": "<page_id>",
    "question": "your question 1",
    "answer": "your answer to question 1",
}

""" + f"""
Now here is the context.
Page ID: {page.id}
Context:
{page.title}\n
{page.text}\n

Create one factoid question with answer about the context above in a json structure.
"""

    # print("Prompt:\n\n" + prompt + "\n\n\n")
    print("\n*******************************************************************************\n")
    print(page.title)
    print("\n*******************************************************************************\n")
    print(page.text)
    print("\n*******************************************************************************\n")
    print(models.chat(prompt, system))
    print("\n*******************************************************************************")
    print("*******************************************************************************")
    print("*******************************************************************************")
    print()
