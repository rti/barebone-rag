import models
import postgres
import json

questions_json = """
[ 
{
  "chunk_id": "8",
  "question": "hackathon 2024 location"
}, 
{
  "chunk_id": "1",
  "question": "hackathon tallinn location"
} 
]
"""

questions = json.loads(questions_json)

for question in questions:
    query = question["question"]
    emb = models.embeddingString(query)
    chunks = postgres.get_similar_chunks(emb, 3)

    result = [c for c in chunks if c.id == int(question["chunk_id"])]

    print("*" * 72)
    print(f"*** {query}")
    print("*" * 72)
    print()

    for c in chunks:
        print("*" * 72)
        print(f"{c.id} {c.title}")
        print("*" * 72)
        print()
        print(c.text)
        print()
        print("*" * 72)
        print("*" * 72)
        print()


    if len(result) > 0:
        print("YAY")
    else:
        print("nope")


