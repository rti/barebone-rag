# Semantic Search and RAG on a FOSS stack

## Slides

➡️ [rti.github.io/barebone-rag/slides.html](https://rti.github.io/barebone-rag/slides.html)

## Quickstart

Required software:

- Docker Engine
- Docker Compose V2

### Start the stack
```
docker compose up --build --wait
```

### Import the goodwiki dataset

Download a goodwiki dump from huggingface https://huggingface.co/datasets/euirim/goodwiki ([direct link](https://huggingface.co/datasets/euirim/goodwiki/resolve/main/09_04_2023_v1.parquet?download=true))

Rename the file to `goodwiki.parquet` and run
```
docker compose run app python import_dump.py
```
This will take some time. But you can start querying already while it's running.

### Start the REPL to query the dataset

```
docker compose run app python repl.py
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

## Generate the slides

```
marp-cli --watch slides.md
```

Or, with [nix-wrap](https://github.com/rti/nixwrap):

```
wrap -n nix run nixpkgs#marp-cli -- --watch slides.md
```

