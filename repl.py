import models
import postgres
from copy import deepcopy
from typing import List, Tuple


def print_chunk_info(chunk, rank):
    url = f"https://en.wikipedia.org/wiki/{chunk.title.replace(' ', '_')}"
    print(f"{chunk.title} ({rank}) {url}")
    print(f"{chunk.description}")


def print_results(chunks_with_distances):
    if len(chunks_with_distances) == 0:
        print("No results found.")
        return

    pages = {}

    chunks_with_distances = deepcopy(chunks_with_distances)

    # merge multiple chunks of the same page, keeping the highest rank
    last_rank = 0
    for chunk, rank in chunks_with_distances:
        assert last_rank < rank, "distances are not sorted."
        last_rank = rank

        existing_chunk = pages.get(chunk.pageId, None)
        if not existing_chunk:
            pages[chunk.pageId] = (chunk, rank)

    print("Results:\n")

    # sort pages by rank and print
    for p in sorted(pages.values(), key=lambda x: x[1]):
        print_chunk_info(p[0], p[1])
        print()


def get_sys_prompt():
    return """
Don't answer questions that are harmful or immoral.
You are a powerful conversational AI trained to help people. You are
augmented by a number of documents, and your job is to use and consume the
documents to best help the user. You will then see a specific instruction
instructing you what kind of response to generate. When you answer the user's
requests, you cite your sources in your answers, according to those
instructions. You should focus on serving the user's needs as best you can,
which will be wide-ranging. You should answer in full sentences, using proper
grammar and spelling.
"""


def get_user_prompt(query, chunks_with_distances: List[Tuple[postgres.Chunk, float]]):
    context = ""
    index = 0
    for c, _ in chunks_with_distances:
        context += f"Document {index}\n{c.title}: {c.description}\n{c.text}\n\n"
        index += 1

    return (
        f"Respond to a query. Base your answer on information from this context only:\n"
        + f"{context}\n\nEnd of context.\n\nRespond to the following query {query}."
    )


def print_chatbot(stream):
    chars = 0

    print()
    for c in stream:
        chunk_of_text: str = c["message"]["content"]

        if "\n" in chunk_of_text:
            chars = 0

        if chars > 79 and " " in chunk_of_text:
            split = chunk_of_text.index(" ")
            chunk_of_text = f"{chunk_of_text[:split]}\n{chunk_of_text[split:].lstrip()}"
            chars = 0

        chars += len(chunk_of_text)

        print(chunk_of_text, end="", flush=True)

    print()


def rag(query, number_of_documents=5):
    emb = models.embedding_string(query, models.EmbeddingPrefix.QUERY)
    chunks_with_distances = postgres.get_similar_chunks_with_distance(
        emb, number_of_documents
    )

    print_results(chunks_with_distances)

    sys_prompt = get_sys_prompt()
    user_prompt = get_user_prompt(query, chunks_with_distances)

    # print(sys_prompt)
    # print(user_prompt)

    stream = models.chat(input=user_prompt, system=[sys_prompt], stream=True)

    print_chatbot(stream)


if __name__ == "__main__":
    while True:
        query = input("\nQuery >> ")
        rag(query, number_of_documents=6)
