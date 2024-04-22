---
title: Semantic Search and RAG on a FOSS stack
author: Robert Timm
footer: Wikimedia Hackathon 2024 Tallinn | Robert Timm | <robert.timm@wikimedia.de>
---

# <!-- fit --> Semantic Search and RAG on a FOSS stack

---

## Semantic Search

Find objects with similar meaning based on a query.

## Retrieval Augmented Generation (RAG)

Create texts based on information loaded from external sources.

## Free and Open Source Software (FOSS) Stack

All software components are released under [OSI approved licenses](https://opensource.org/licenses).

---

# Components for Semantic Search

- Measure Similarity (embeddings)
- Database to store information (database)
- Find most similar items (vector search)

---

# Embedding Models

|                                                                                   | OSI License   | Pre Train Data | Fine Tune Data |
| --------------------------------------------------------------------------------- | ------------- | -------------- | -------------- |
| [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | ✅ Apache-2.0 | ✅             | ✅             |
| [nomic-embed-text-v1](https://huggingface.co/nomic-ai/nomic-embed-text-v1)        | ✅ Apache-2.0 | ✅             | ✅             |
| [mxbai-embed-large-v1](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1) | ✅ Apache-2.0 | ⛔             | ⛔             |

---

# Embedding Inference

## [🦙 Ollama](https://github.com/ollama/ollama)

_Get up and running with large language models._

- Inference engine based on [llama.cpp](https://github.com/ggerganov/llama.cpp)
- Supports CPU and AMD - `amdgpu` and ROCm are MIT licensed ✅
- Quantization
- Model Library
- One model, one inference at a time

---

# Embedding Inference

|                                                                                          | OSI License   | ROCm support | Production |
| ---------------------------------------------------------------------------------------- | ------------- | ------------ | ---------- |
| [Ollama](https://github.com/ollama/ollama)                                               | ✅ MIT        | ✅           | ⛔         |
| [llama.cpp](https://github.com/ggerganov/llama.cpp)                                      | ✅ MIT        | ✅           | ⛔         |
| [HF Text Embeddings Interface](https://github.com/huggingface/text-embeddings-inference) | ✅ Apache-2.0 | ⛔           | ✅         |
| [Infinity](https://github.com/michaelfeil/infinity)                                      | ✅ MIT        | ✅           | ✅         |

---

# Embedding Implementation

#### Start ollama
```sh
$ ollama serve &
$ ollama pull nomic-embed-text-v1
```
#### Generate embedding
```python
import ollama # pip install ollama

res = ollama.embeddings(
    model="nomic-embed-text-v1",
    prompt="This string")

res["embedding"] # [0.33, 0.62, 0.19, ...]
```

---

# Vector Database

🐘 Postgres can do it 🎉

## [pgvecto.rs](https://github.com/tensorchord/pgvecto.rs)

_Scalable, Low-latency and Hybrid-enabled Vector Search in Postgres._

A PostgreSQL extension written in Rust.

<!-- TODO: what is hybrid-enabled https://pgvecto-rs-docs-git-fork-gaocegege-hybrid-tensorchord.vercel.app/use-cases/hybrid-search.html -->

---

# Vector Database Licensing

|             | OSI License           |
| ----------- | --------------------- |
| PostgreSQL  | ✅ PostgreSQL License |
| pgvector.rs | ✅ Apache-2.0         |

---

# Vector Database Implementation

#### Create PostgreSQL table using vecto.rs
```sql
CREATE EXTENSION vectors;
CREATE TABLE IF NOT EXISTS chunks ( 
  id SERIAL PRIMARY KEY, 
  text TEXT NOT NULL, 
  embedding VECTOR( 384 ) NOT NULL
);
```

#### Find most similar chunks
```sql
SELECT id, text FROM chunks 
  ORDER BY embedding <-> [0.33, 0.62, 0.19, ...] 
  LIMIT 5;
```

---

# <!-- fit --> Components for Retrieval Augmented Generation

- Semantic Search
- Large Language Model (LLM) for Generation

---

# LLM Inference

## [🦙 Ollama](https://github.com/ollama/ollama)
- again 😀

---

# Model Inference Licenses

|                                                                                          | OSI License   | ROCm Support | Production |
| ---------------------------------------------------------------------------------------- | ------------- | ------------ | ---------- |
| [Ollama](https://github.com/ollama/ollama)                                               | ✅ MIT        | ✅           | ⛔         |
| [llama.cpp](https://github.com/ggerganov/llama.cpp)                                      | ✅ MIT        | ✅           | ⛔         |
| [vllm](https://github.com/vllm-project/vllm)                                             | ✅ Apache-2.0 | ✅           | ✅         |
| [HF Text Generation Interface](https://github.com/huggingface/text-generation-inference) | ✅ Apache-2.0 | ✅           | ✅         |

---

# LLMs with Openly Licensed Weights

| Model Name                                                                             | License         | Pre Train Data | Fine Tune Data |
| -------------------------------------------------------------------------------------- | --------------- | -------------- | -------------- |
| [Mistral 0.2 7b](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)            | ✅ Apache-2.0   | ⛔             | ⛔             |
| [HF Zephyr 7b beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)               | ✅ MIT          | ⛔             | ✅             |
| [OpenChat 7b 3.5](https://huggingface.co/openchat/openchat-3.5-0106)                   | ✅ Apache-2.0   | ⛔             | ✅             |
| [Cohere Command-R 35b](https://huggingface.co/CohereForAI/c4ai-command-r-v01)          | ✅ CC-BY-NC 4.0 | ⛔             | ⛔             |
| [Stability.AI StableLM2 1.6b](https://huggingface.co/stabilityai/stablelm-2-1_6b-chat) | ⛔ Custom       | ✅             | ✅             |
| [Olmo](https://huggingface.co/allenai/OLMo-7B)                                         |                 |                |

---

# Other Famous LLMs with "free" weights

| Model Name                                                           | License   | Pre Train Data | Fine Tune Data |
| -------------------------------------------------------------------- | --------- | -------------- | -------------- |
| [Meta Llama 3 8b](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | ⛔ Custom | ⛔             | ⛔             |
| [Google Gemma 1.1 7b](https://huggingface.co/google/gemma-1.1-7b-it) | ⛔ Custom | ⛔             | ⛔             |
| [Alibaba Qwen 1.5 7b](https://huggingface.co/Qwen/Qwen1.5-7B)        | ⛔ Custom | ⛔             | ⛔             |

---

# Notable LLMs with Open Weights Licenses

---
