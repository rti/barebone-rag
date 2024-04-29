from tqdm import tqdm

import models
import postgres
import chunker

import pyarrow.parquet as pq

postgres.init(embeddingLength=models.embeddingLength())

with postgres.get_connection().cursor() as cur:
    # https://huggingface.co/datasets/euirim/goodwiki
    table = pq.read_table('./goodwiki.parquet')
    df = table.to_pandas()

    for index, row in tqdm(df.iterrows(), total=len(df)):
        title = row['title']
        desc = row['description']
        text = row['markdown']

        cur.execute(
            "INSERT INTO pages (title, description, text) VALUES (%s, %s, %s) RETURNING id;",
            (title, desc, text),
        )
        result = cur.fetchall()
        pageId = result[0][0]

        for c in chunker.chunk(text, chunkSize=256, overlap=32):
            chunkText = title + "\n" + (desc if desc else "") + "\n" + c
            embedding = models.embeddingString(chunkText, models.EmbeddingPrefix.DOCUMENT)
            cur.execute(
                "INSERT INTO chunks (text, embedding, page_id) VALUES (%s, %s, %s);",
                (c, embedding, pageId),
            )

        # Commit the transaction
        postgres.get_connection().commit()

postgres.get_connection().close()
