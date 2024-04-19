import models
import postgres

print("**************************************************")

query = "software feature delivery"
emb = models.embeddingString(query)
chunks = postgres.get_similar_chunks(emb, 5)

system = "You are a helpful assistant. \
        You base your knowledge of data that is given in a context \
        marked with CONTEXT_BEGIN and CONTEXT_END."

prompt = f"""
CONTEXT_BEGIN

{"CHUNK\n" + "\n\nCHUNK\n\n".join([c.text for c in chunks])}

CONTEXT_END

Summarize each CHUNK in between CONTEXT_BEGIN and CONTEXT_END with respect to: {query}
"""
print("Prompt:\n\n" + prompt + "\n\n\n")

print("**************************************************")
result = models.chat(prompt, system)
print(result)
print("**************************************************")

# prompt2 = f"""Given the following context:\n\n
#
# Begin of context
#
# {result}
#
# End of context
#
# Your task: Try to derive as much information as possible from the context to everything related to:
# {query}
# """
# print("Prompt 2: " + prompt2)
# print(
#     "********************************************************************************"
# )
# result2 = models.chat(prompt2)
# print(result2)
