import psycopg
from psycopg.sql import SQL, Literal

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
                title VARCHAR(255) NOT NULL, 
                text TEXT NOT NULL, 
                embedding vector( {} ) NOT NULL
            );
            """
        ).format(Literal(str(embeddingLength)))
    )
    db.commit()
