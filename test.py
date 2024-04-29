import models
import postgres
import repl
import time


if __name__ == "__main__":
    print(64 * ".")

    # query = "adjustment of dna"
    query = "scandinavian wild tiger"
    print("Query:", query)

    # measure time to search
    start = time.time()

    emb = models.embeddingString(query, models.EmbeddingPrefix.QUERY)
    end = time.time()
    print(f"Embeddings after {round((end - start), 1)}s")

    chunksWithRanks = postgres.get_similar_chunks_with_rank(emb, 10)
    end = time.time()
    print(f"Results after {round((end - start), 1)}s")

    print()
    repl.print_results(chunksWithRanks)


