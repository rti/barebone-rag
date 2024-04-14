import mwxml
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="postgres",
    database="mydb",
    user="myuser",
    password="mypassword"
)

# Begin a transaction
conn.autocommit = False

# Create a cursor object to execute queries
cur = conn.cursor()


# Create a table to store the page text
cur.execute("""
CREATE TABLE IF NOT EXISTS page_text (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    text TEXT NOT NULL
);
""")

# Open the MediaWiki XML dump
with open("dump.xml", "rb") as f:
    # Create a Dump object
    dump = mwxml.Dump.from_file(f)

    # Iterate over the pages in the dump
    for page in dump.pages:
        # Get the page title and text
        title = page.title

        text = ""

        # We support only one revision in the dump
        for revision in page: text = revision.text

        print(title)
        print(text)


        # Delete the existing page from the table
        cur.execute("DELETE FROM page_text WHERE title = %s;", (title,))

        if text.startswith("#REDIRECT"): continue

        # Insert the page text into the database
        cur.execute("""
        INSERT INTO page_text (title, text)
        VALUES (%s, %s);
        """, (title, text))

        # Commit the changes
        conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
