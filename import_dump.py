import mwxml
import psycopg2
import ollama
from tqdm import tqdm
import re


ollamaConnection = ollama.Client(host="ollama:11434")

embeddingsModel = "all-minilm" # mxbai-embed-large
ollamaConnection.pull(model=embeddingsModel)

dbConnection = psycopg2.connect(
    host="postgres",
    database="mydb",
    user="myuser",
    password="mypassword"
)
dbConnection.autocommit = False
dbCursor = dbConnection.cursor()
# dbCursor.execute(f"""
# DROP EXTENSION IF EXISTS vectors;
# CREATE EXTENSION vectors;
# """)

# Create a table to store the page text including embeddings
embedding = ollamaConnection.embeddings(model=embeddingsModel, prompt="embed this!")
embeddingLength = len(embedding.get('embedding')) # type: ignore # ollama gets something wrong here
dbCursor.execute(f"""
CREATE TABLE IF NOT EXISTS page_text (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    embedding vector({embeddingLength}) NOT NULL
);
""")

with open("dump.xml", "rb") as f:
    dump = mwxml.Dump.from_file(f)

    for page in tqdm(dump.pages):
        title = page.title
        if title is None: continue
        if re.search("/[a-z][a-z][a-z]?(-[a-z]+)?$", title):
            print(f"skipping {title}")
            continue

        text = list(page)[0].text # We support only one revision in the dump
        # for revision in page: text = revision.text

        if text is None: continue

        # Delete existing page chunks, that is, update if we know about it already
        dbCursor.execute("DELETE FROM page_text WHERE title = %s;", (title,))

        # ignore redirect pages
        if text.strip().lower().startswith("#redirect"): continue

        embeddingsResult = ollamaConnection.embeddings(model=embeddingsModel, prompt=text)
        embedding = embeddingsResult['embedding']; # type: ignore # ollama gets something wrong here
        embeddingString = "[" + ", ".join([str(num) for num in embedding]) + "]"

        # Insert the page text into the database
        dbCursor.execute("INSERT INTO page_text (title, text, embedding) VALUES (%s, %s, %s);", 
                         (title, text, embeddingString))

        # Commit the transaction
        dbConnection.commit()

# Close the cursor and connection
dbCursor.close()
dbConnection.close()
