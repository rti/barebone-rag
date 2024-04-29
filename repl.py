import models
import postgres

def print_chunk_info(chunk, rank):
    print(f"{chunk.title} - {rank}")
    print(f"{chunk.description}")

def print_results(chunks_with_ranks):
    if len(chunks_with_ranks) == 0:
        print("No results found.")
        return

    for (chunk, rank) in chunks_with_ranks:
        print("=========================")
        print_chunk_info(chunk, rank)

    print("=========================")

if __name__ == "__main__":
    while True:
        query = input("\nQuery >> ")
        emb = models.embeddingString(query)
        print(f"{emb}")
        chunks = postgres.get_similar_chunks(emb, 10)
        print_results(chunks)
