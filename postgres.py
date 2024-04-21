import psycopg
from psycopg.sql import SQL, Literal
from typing import List
from dataclasses import dataclass

_db: psycopg.Connection | None = None


def get_connection() -> psycopg.Connection:
    global _db
    if not _db:
        _db = psycopg.connect("postgresql://myuser:mypassword@postgres/mydb")
        _db.autocommit = False

    return _db


def init(embeddingLength: int):
    if not isinstance(embeddingLength, int) or embeddingLength <= 0:
        raise ValueError("Invalid embedding length")

    db = get_connection()
    cur = db.cursor()

    try:
        cur.execute("CREATE EXTENSION vectors;")
    except psycopg.errors.Error:
        print("extension 'vector' already exists.")
    db.commit()

    cur.execute(
        SQL(
            """
            CREATE TABLE IF NOT EXISTS pages ( 
                id SERIAL PRIMARY KEY, 
                title VARCHAR(255) NOT NULL, 
                text TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS chunks ( 
                id SERIAL PRIMARY KEY, 
                page_id INT NOT NULL, 
                title VARCHAR(255) NOT NULL, 
                text TEXT NOT NULL, 
                embedding vector( {} ) NOT NULL
            );
            """
        ).format(Literal(str(embeddingLength)))
    )
    db.commit()


@dataclass
class Chunk:
    text:str


def get_similar_chunks(embeddingString: str, numberOfResults=5) -> List[Chunk]:
    cur = get_connection().cursor()
    cur.execute(
        "SELECT text FROM chunks ORDER BY embedding <-> %s LIMIT %s;",
        (
            embeddingString,
            numberOfResults,
        ),
    )
    res = cur.fetchall()
    cur.close()

    return [Chunk(text=r[0]) for r in res]


@dataclass
class Page:
    title: str
    text: str


def get_pages(limit=10) -> List[Page]:
    cur = get_connection().cursor()
    cur.execute(
        "SELECT title, text FROM pages LIMIT %s;",
        (limit,),
    )
    res = cur.fetchall()
    cur.close()

    return [Page(title=r[0], text=r[1]) for r in res]

