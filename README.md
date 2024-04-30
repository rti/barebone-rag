# Semantic Search and RAG on a FOSS stack

## Slides
[rti.github.io/barebone-rag/slides.html](https://rti.github.io/barebone-rag/slides.html)

## Quickstart

Required software:
- Docker Engine
- Docker Compose



### Start the stack
```
docker compose up --build
```

### Import a MediaWiki Dump

Will import from `./dump.xml`.
```
docker compose run --build app import_dump.py
```
This will take some time. On a 12th gen Intel without GPU importing a full dump from mediawiki.org took about 4h.

### Generate the slides
```
marp-cli --watch slides.md
```
Or, with nix-wrap:

```
wrap -n nix run nixpkgs#marp-cli -- --watch slides.md
```

## Development
### Python dependencies
```
pip install beautifulsoup4
pip install black
pip install lxml
pip install ollama
pip install psycopg[binary]
pip install tqdm
```

or


```
pip install -r requirements.txt
```
