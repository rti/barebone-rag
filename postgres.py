import psycopg
from psycopg.sql import SQL, Literal
from typing import List, Tuple
from dataclasses import dataclass

_db: psycopg.Connection | None = None


@dataclass
class Page:
    id: int
    title: str
    description: str
    text: str


@dataclass
class Chunk:
    id: int
    pageId: int
    title: str
    description: str
    text: str


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
                description VARCHAR(255), 
                text TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS chunks ( 
                id SERIAL PRIMARY KEY, 
                page_id INT NOT NULL, 
                text TEXT NOT NULL, 
                embedding vector( {} ) NOT NULL
            );
            """
        ).format(Literal(str(embeddingLength)))
    )
    db.commit()


def get_similar_chunks_with_distance(
    embeddingString: str, limit=5
) -> List[Tuple[Chunk, float]]:
    """<-> in pgvecto.rs is squared euclidean distance as metric"""

    cur = get_connection().cursor()
    cur.execute(
        """
        SELECT 
            c.id, c.page_id, p.title, p.description, c.text, 
            c.embedding <-> %s AS distance
        FROM chunks c
        JOIN pages p ON c.page_id = p.id
        ORDER BY c.embedding <-> %s
        LIMIT %s;
        """,
        (
            embeddingString,
            embeddingString,
            limit,
        ),
    )
    res = cur.fetchall()
    cur.close()

    return [
        (
            Chunk(id=r[0], pageId=r[1], title=r[2], description=r[3], text=r[4]),
            float(r[5]),
        )
        for r in res
    ]
