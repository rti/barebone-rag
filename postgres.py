import psycopg

_db: psycopg.Connection | None = None


def get_connection() -> psycopg.Connection:
    global _db
    if not _db:
        _db = psycopg.connect("postgresql://myuser:mypassword@postgres/mydb")
        _db.autocommit = False

    return _db


def init(embeddingLength: int):
    db = get_connection()
    cur = db.cursor()

    try:
        cur.execute("CREATE EXTENSION vectors;")
    except psycopg.errors.Error:
        print("extension 'vector' already exists.")
    db.commit()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS page_text ( 
            id SERIAL PRIMARY KEY, 
            title VARCHAR(255) NOT NULL, 
            text TEXT NOT NULL, 
            embedding vector( %s ) NOT NULL);
        """,
        (embeddingLength,),
    )
    db.commit()
