import ml
import postgres

# print(ml.chat("What is the meaning of life?"))

query = "event 2024 tallinn"
emb = ml.embeddingString(query)
cur = postgres.get_connection().cursor()
cur.execute("SELECT text FROM page_text ORDER BY embedding <-> %s LIMIT 5;", (emb,))
res = cur.fetchall()

context = "\n".join([r[0] for r in res])

print("********************************************************************************")
print("********************************************************************************")
print("********************************************************************************")
prompt = f"""{context}\n\n
Summarize the above text, focus on infomation related to: {query}
"""
print("Prompt: " + prompt + "\n\n\n")

print("********************************************************************************")
result = ml.chat(prompt)
print(result)

print("********************************************************************************")
prompt2 = f"""Given the following context:\n\n

Begin of context

{result}

End of context

Your task: Try to derive as much information as possible from the context to everything related to:
{query}
"""
print("Prompt 2: " + prompt2)
print("********************************************************************************")
result2 = ml.chat(prompt2)
print(result2)

