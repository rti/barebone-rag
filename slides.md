---
title: Semantic Search and RAG on a FOSS stack
author: Robert Timm
---

<!-- footer: -->

![bg right](./slides_code_qrcode.png)

# Semantic Search and RAG on a FOSS stack

Wikimedia Hackathon Tallinn 2024

### [github.com/rti/barebone-rag](https://github.com/rti/barebone-rag)

Robert Timm <robert.timm@wikimedia.de>

---

<!-- paginate: true -->
<!-- header: Semantic Search and RAG on a FOSS stack -->

## Semantic Search

Given a query, find texts with a meaning similar.

## Retrieval Augmented Generation (RAG)

Create texts based on information loaded from external sources.

## Free and Open Source Software (FOSS) Stack

All software components are released under [OSI approved licenses](https://opensource.org/licenses).

---

# <!-- fit --> Demo Time

---


# GPU stacks

- ⛔ NVIDIA CUDA has a proprietary license
- ✅ AMD ROCm stack is MIT licensed
  - `amdgpu` driver in kernel mainline

---

# Components for Semantic Search

- Encode semantics ▶ **Embeddings**
- Find semantically similar objects ▶ **Vector Database**

---

# Embedding Models

|                                                                                   | Dims | OSI License   | Pre Train Data | Fine Tune data |
| --------------------------------------------------------------------------------- | ---- | ------------- | -------------- | -------------- |
| [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | 384  | ✅ Apache-2.0 | ✅             | ✅             |
| [nomic-embed-text-v1](https://huggingface.co/nomic-ai/nomic-embed-text-v1)        | 768  | ✅ Apache-2.0 | ✅             | ✅             |
| [bge-large-en-v1.5](https://huggingface.co/BAAI/bge-large-en-v1.5)                | 1024 | ✅ MIT        | ⛔             | ⛔             |
| [mxbai-embed-large-v1](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1) | 1024 | ✅ Apache-2.0 | ⛔             | ⛔             |

<!-- footer: "Find more embedding models here: https://huggingface.co/spaces/mteb/leaderboard" -->

---

<!-- footer: "" -->

# Embedding Inference

## [🦙 Ollama](https://github.com/ollama/ollama)

_Get up and running with large language models._

- Inference engine based on [llama.cpp](https://github.com/ggerganov/llama.cpp)
- Supports AMD GPU via ROCm
- CPU support (AVX, AVX2, AVX512, Apple Silicon)
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

<!-- footer: "More code: https://github.com/rti/barebone-rag/blob/main/models.py" -->

---

# Vector Database

🐘 Postgres can do it 🎉

## [pgvecto.rs](https://github.com/tensorchord/pgvecto.rs)

_Scalable, Low-latency and Hybrid-enabled Vector Search in Postgres._

A PostgreSQL extension written in Rust.

<!-- TODO: what is hybrid-enabled https://pgvecto-rs-docs-git-fork-gaocegege-hybrid-tensorchord.vercel.app/use-cases/hybrid-search.html -->
<!-- footer: "" -->

---

# Vector Database Licensing

|             | OSI License           |
| ----------- | --------------------- |
| PostgreSQL  | ✅ PostgreSQL License |
| pgvector.rs | ✅ Apache-2.0         |

<!-- footer: "Find more options here: https://ann-benchmarks.com/" -->

---

# Vector Database Implementation

#### Create PostgreSQL table using pgvecto.rs

```sql
CREATE EXTENSION vectors;

CREATE TABLE chunks (
  text TEXT NOT NULL,
  embedding VECTOR( 768 ) NOT NULL
);
```

#### Find most similar chunks

```sql
SELECT text FROM chunks
  ORDER BY embedding <-> [0.33, 0.62, 0.19, ...]
  LIMIT 5;
```

<!-- footer: "More code: https://github.com/rti/barebone-rag/blob/main/postgres.py" -->

---

# <!-- fit --> Components for Retrieval Augmented Generation (RAG)

- Find matching sources ▶ **Semantic Search**
- Generate Response ▶ **Large Language Model (LLM) Inference**

<!-- footer: "" -->

---

# LLM Inference

## [🦙 Ollama](https://github.com/ollama/ollama)

- LLMs too 😀 Actually its core use case
- Great [model library](https://ollama.com/library) 📚

---

# LLM Inference

|                                                                                          | OSI License   | ROCm Support | Production |
| ---------------------------------------------------------------------------------------- | ------------- | ------------ | ---------- |
| [Ollama](https://github.com/ollama/ollama)                                               | ✅ MIT        | ✅           | ⛔         |
| [llama.cpp](https://github.com/ggerganov/llama.cpp)                                      | ✅ MIT        | ✅           | ⛔         |
| [vllm](https://github.com/vllm-project/vllm)                                             | ✅ Apache-2.0 | ✅           | ✅         |
| [HF Text Generation Interface](https://github.com/huggingface/text-generation-inference) | ✅ Apache-2.0 | ✅           | ✅         |

---

# LLM Inference Implementation

Generate a text based on a prompt

```python
import ollama # pip install ollama

res = ollama.chat(
    model="zephyr:7b-beta",
    messages=[{"role": "user", "content": f"Summarize this text: {text}"}],
    stream=False,
)
res["message"]["content"] # "The given text..."
```

<!-- footer: "More code: https://github.com/rti/barebone-rag/blob/main/models.py" -->

---

# Large Language Model Building Blocks

- Weights (binary)
- Pre training (source)
- Fine tuning data (source)
- Training code (build scripts)

---

# OSI - Open Source AI Initiative

- Intends to define Open Source models
- Defines which parts need to have [OSD](https://opensource.org/osd)-compliant licenses
- Draft, Release planned for October 2024
- [Latest draft (April 2024)](https://opensource.org/deepdive/drafts/the-open-source-ai-definition-draft-v-0-0-8)
  - Marks training data sets as optional
  - But requires data characteristics, labeling procedures, etc.

---

# LLMs with Openly Licensed Weights

|                                                                                      | OSI Weights   | PT Data | FT Data | Code |
| ------------------------------------------------------------------------------------ | ------------- | ------- | ------- | ---- |
| [Mistral 0.2 7b](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)          | ✅ Apache-2.0 | ⛔      | ⛔      | ⛔   |
| [HF Zephyr 7b beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)             | ✅ MIT        | ⛔      | ✅      | ✅   |
| [Microsoft Phi-3 Mini 3.8b](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) | ✅ MIT        | ⛔      | ⛔      | ⛔   |
| [Apple ELM 3b](https://huggingface.co/apple/OpenELM)                                 | ⛔❓ASCL      | ✅      | ✅      | ✅   |
| [Meta Llama 3 8b](https://huggingface.co/meta-llama/Meta-Llama-3-8B)                 | ⛔ Custom     | ⛔      | ⛔      | ⛔   |
| [Google Gemma 1.1 7b](https://huggingface.co/google/gemma-1.1-7b-it)                 | ⛔ Custom     | ⛔      | ⛔      | ⛔   |

_PT: pre-training - FT: fine tuning_

<!-- footer: "Find more LLMs here: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard" -->

---

# Open Source LLM Projects

- [Bloom](<https://en.wikipedia.org/wiki/BLOOM_(language_model)>) (2022), BigScience RAIL License v1.0, not SOTA, not OSD
- [Allan AI OLMo](https://huggingface.co/allenai/OLMo-7B) based on the [Dolma dataset](https://huggingface.co/datasets/allenai/dolma)
- [LumiOpen Viking](https://huggingface.co/LumiOpen/Viking-7B) built on [Lumi Supercomputer](https://www.lumi-supercomputer.eu/)
- [HuggingFace StarChat2](https://huggingface.co/HuggingFaceH4/starchat2-15b-v0.1) focussed on code
- [OpenGPT-X](https://opengpt-x.de/en/project/) EU funded

---

# Conclusion

- ✅ Almost all software components are available with OSI approved licenses
- ✅ ROCm works and people are using it
- ❓ Definition of open source models unclear
- 🤔 Identifying truly open source models is complicated
- ⏳ Interesting developments ongoing

<!-- footer: "" -->
