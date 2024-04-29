import models
import postgres
import repl


# query = "adjustment of dna"
query = "scandinavian wild tiger"
emb = models.embeddingString(query, models.EmbeddingPrefix.QUERY)
print(emb)
chunksWithRanks = postgres.get_similar_chunks_with_rank(emb, 10)
repl.print_results(chunksWithRanks)

