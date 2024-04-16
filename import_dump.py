import mwxml
import bs4
import tqdm
import re

import ml
import postgres

def strip_wikitext(s):
    HTML_FILTERS  = {
        'div': ['navbox','navbox-styles','spoken-wikipedia', 'noprint', 'hatnote', 'rt-tooltip', 'reflist'],
        'span': ['mw-ext-cite-error'],
        'table': ['noprint','ombox'],
        'ol': ['breadcrumb-nav-container', 'references'],
        'sup': ['reference']
    }
    REGEX_FILTERS = {
        'p': '→.*ersion'
    }

    def filterHtml(soup):
        for figure in soup.find_all('figure'):
            figure.decompose()

        for tag, classes in HTML_FILTERS.items():
            for className in classes:
                for div in soup.find_all(tag, {'class': className}):
                    div.decompose()

        for tag, regex in REGEX_FILTERS.items():
            for element in soup.find_all(tag):
                if(re.search(regex, str(element)) != None):
                    element.decompose()

        return soup

    if s is None: return None

    section_soup = bs4.BeautifulSoup(s, 'lxml')
    text = filterHtml(section_soup).get_text()
    text = text.strip()

    if len(text) == 0: return None
    if text.lower().startswith("#redirect"): return None

def chunk(s: str):
    words = s.split(" ")
    CHUNK_SIZE = 256
    OVERLAP = 64
    return [" ".join(words[i:i+CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE - OVERLAP)]

# cases = [
#     (
#         "",
#         [""],
#     ),
#     (
#         "hi",
#         ["hi"],
#     ),
#     (
#         "this is a test",
#         ["this is a test"],
#     ),
#     (
#         "this is a long test with more than ten words so that we can test overlap",
#         [
#             "this is a long test with more than ten words",
#             "ten words so that we can test overlap",
#         ],
#     ),
# ]
#
#
# for case in cases:
#     print("Testing chunk function.")
#     print("Input: %s" % str(case))
#     outexp = case[1]
#     outactual = chunk(case[0])
#     assert outactual == outexp, "%s != %s" % (outactual, outexp)
#
postgres.init(embeddingLength=ml.embeddingLength())

with postgres.get_connection().cursor() as cur:
    with open("dump.xml", "rb") as f:
        dump = mwxml.Dump.from_file(f)

        for page in tqdm.tqdm(dump.pages):
            title = page.title
            if title is None: continue
            if re.search("/[a-z][a-z][a-z]?(-[a-z]+)?$", title):
                # print(f"skipping {title}")
                continue

            # Delete existing page chunks, that is, update if we know about it already
            cur.execute("DELETE FROM page_text WHERE title = %s;", (title,))

            # We support only one revision in the dump
            text = list(page)[0].text

            text = strip_wikitext(text)
            if text is None: continue

            for c in chunk(text):
                embedding = ml.embedding(c)
                embeddingString = "[" + ", ".join([str(num) for num in embedding]) + "]"
                cur.execute("INSERT INTO page_text (title, text, embedding) VALUES (%s, %s, %s);",
                            (title, c, embeddingString))

            # Commit the transaction
            postgres.get_connection().commit()

postgres.get_connection().close()
