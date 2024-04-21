import models
import postgres
import json

question_json = """
{
    "page_id": "<page_id>",
    "question": "your question 1",
    "answer": "your answer to question 1",
}
"""

question = json.loads(question_json)

query = question["question"]
emb = models.embeddingString(query)
chunks = postgres.get_similar_chunks(emb, 5)

result = list(filter(lambda c: c.pageId == question["page_id"], chunks))

if len(result) > 0:
    print("YAY")
else:
    print("nope")
