import models
import postgres

pages = postgres.get_pages()

system = """\
You are a generating questions.
You will be provided with texts. 
You task is to generate questions, that can be answered by the text given.
"""

for page in pages:
    prompt = f"""\
Given the following text:

{page.title}
{page.text}

Generate 3 questions that this text can answer."""

    print("Prompt:\n\n" + prompt + "\n\n\n")
    print(models.chat(prompt, system))
    print()
