import models
import postgres
import json

questions_json = """
[ 
{ "question": "What gate in the Marrakesh medina has an interior passage with multiple turns, and what is its name?", "chunk-id": "35845" },
{ "question": "What technology did Takashi Kurita's team use to create fluid and varied sprite animations in Princess Crown 1997, despite hardware limitations on the Saturn console?", "chunk-id": "89434" },
{ "question": "Question: What significant decision did Jan Smuts make in June 1895, as his Ebden funding came to an end, that determined his future career path?", "chunk-id": "13838" },
{ "question": "Takashi Kurita fluid animations", "chunk-id": "89434" }
]
"""

questions = json.loads(questions_json)

for question in questions:
    query = question["question"]
    emb = models.embedding_string(query)
    chunks = postgres.get_similar_chunks(emb, 3)

    result = [c for c in chunks if c.id == int(question["chunk-id"])]

    print("*" * 72)
    print(f"*** {query}")
    print("*" * 72)
    print()

    for c in chunks:
        print("*" * 72)
        print(f"{c.id} {c.title}")
        # print("*" * 72)
        # print()
        # print(c.text)
        # print()
        # print("*" * 72)
        print("*" * 72)
        print()


    if len(result) > 0:
        print("YAY")
    else:
        print("nope")

    print()
    print()


