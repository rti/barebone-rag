import mwxml
import bs4
import tqdm
import re

import models
import postgres
import chunker


def strip_wikitext(s):
    HTML_FILTERS = {
        "div": [
            "navbox",
            "navbox-styles",
            "spoken-wikipedia",
            "noprint",
            "hatnote",
            "rt-tooltip",
            "reflist",
        ],
        "span": ["mw-ext-cite-error"],
        "table": ["noprint", "ombox"],
        "ol": ["breadcrumb-nav-container", "references"],
        "sup": ["reference"],
    }
    REGEX_FILTERS = {"p": "→.*ersion"}

    def filterHtml(soup):
        for figure in soup.find_all("figure"):
            figure.decompose()

        for tag, classes in HTML_FILTERS.items():
            for className in classes:
                for div in soup.find_all(tag, {"class": className}):
                    div.decompose()

        for tag, regex in REGEX_FILTERS.items():
            for element in soup.find_all(tag):
                if re.search(regex, str(element)) != None:
                    element.decompose()

        return soup

    if s is None:
        return None

    soup = bs4.BeautifulSoup(s, "lxml")
    text = filterHtml(soup).get_text()
    text = text.strip()

    if len(text) == 0:
        return None
    if text.lower().startswith("#redirect"):
        return None

    return text


postgres.init(embeddingLength=models.embedding_length())

with postgres.get_connection().cursor() as cur:
    with open("dump.xml", "rb") as f:
        dump = mwxml.Dump.from_file(f)

        for page in tqdm.tqdm(dump.pages):
            title = page.title
            if title is None:
                continue
            if re.search("/[a-z][a-z][a-z]?(-[a-z]+)?$", title):
                # print(f"skipping {title}")
                continue

            # Delete existing page chunks, that is, update if we know about it already
            cur.execute("DELETE FROM chunks WHERE title = %s;", (title,))
            cur.execute("DELETE FROM pages WHERE title = %s;", (title,))

            # We support only one revision in the dump
            text = list(page)[0].text

            text = strip_wikitext(text)
            if text is None:
                continue

            cur.execute(
                "INSERT INTO pages (title, text) VALUES (%s, %s) RETURNING id;",
                (title, text),
            )
            result = cur.fetchall()
            pageId = result[0][0]

            for c in chunker.chunk(text):
                embedding = models.embedding_string(c)
                cur.execute(
                    "INSERT INTO chunks (title, text, embedding, page_id) VALUES (%s, %s, %s, %s);",
                    (title, c, embedding, pageId),
                )

            # Commit the transaction
            postgres.get_connection().commit()

postgres.get_connection().close()
