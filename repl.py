import models
import postgres


def print_chunk_info(chunk, rank):
    print(f"{chunk.title} ({rank})")
    print(f"{chunk.description}")


def print_results(chunks_with_ranks):
    if len(chunks_with_ranks) == 0:
        print("No results found.")
        return

    pages = {}

    # merge chunk-ranks of multiple pages into one to have more concise output
    for chunk, rank in chunks_with_ranks:
        existing_chunk = pages.get(chunk.pageId, None)
        if not existing_chunk:
            pages[chunk.pageId] = (chunk, rank)
        else:
            pages[chunk.pageId] = (existing_chunk[0], min(existing_chunk[1], rank))

    # sort pages by rank and print
    for p in sorted(pages.values(), key=lambda x: x[1]):
        print_chunk_info(p[0], p[1])
        print()


if __name__ == "__main__":
    while True:
        query = input("\nQuery >> ")
        emb = models.embeddingString(query)
        print(f"{emb}")
        chunks = postgres.get_similar_chunks(emb, 10)
        print_results(chunks)
