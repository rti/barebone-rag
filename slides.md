---
title: Semantic Search and RAG on a FOSS stack
author: Robert Timm
---

<!-- footer: Wikimedia Hackathon 2024 Tallinn | Robert Timm | <robert.timm@wikimedia.de> -->

# <!-- fit --> Semantic Search and RAG on a FOSS stack

---

<!-- footer: "" -->

![bg right](./slides_code_qrcode.png)

### [github.com/rti/barebone-rag](https://github.com/rti/barebone-rag)

- Slides
- Example code

---

<!-- paginate: true -->
<!-- header: Semantic Search and RAG on a FOSS stack -->

## Semantic Search

Find objects with similar meaning based on a query.

## Retrieval Augmented Generation (RAG)

Create texts based on information loaded from external sources.

## Free and Open Source Software (FOSS) Stack

All software components are released under [OSI approved licenses](https://opensource.org/licenses).

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
  embedding VECTOR( 384 ) NOT NULL
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

# Large Language Models - open source?

- What is the source of a language model?
  - Pre training data
  - Fine tuning data
  - Training code
  - Weights

---

# LLMs with Openly Licensed Weights

|                                                                                        | License         | Pre Train Data | Fine Tune Data |
| -------------------------------------------------------------------------------------- | --------------- | -------------- | -------------- |
| [Mistral 0.2 7b](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)            | ✅ Apache-2.0   | ⛔             | ⛔             |
| [HF Zephyr 7b beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)               | ✅ MIT          | ⛔             | ✅             |
| [OpenChat 7b 3.5](https://huggingface.co/openchat/openchat-3.5-0106)                   | ✅ Apache-2.0   | ⛔             | ✅             |
| [Cohere Command-R 35b](https://huggingface.co/CohereForAI/c4ai-command-r-v01)          | ✅ CC-BY-NC 4.0 | ⛔             | ⛔             |
| [Stability.AI StableLM2 1.6b](https://huggingface.co/stabilityai/stablelm-2-1_6b-chat) | ⛔ Custom       | ✅             | ✅             |
| [Apple ELM](https://elm)                                                               |                 |                |                |
| [Microsoft Phi-3](https://)                                                            |                 |                |                |

<!-- TODO: apple models -->
<!-- TODO: microsoft phi 3 -->
<!-- footer: "Find more LLMs here: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard" -->

---

<!-- footer: "" -->

# Famous LLMs with "free" weights

| Model Name                                                           | License   | Pre Train Data | Fine Tune Data |
| -------------------------------------------------------------------- | --------- | -------------- | -------------- |
| [Meta Llama 3 8b](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | ⛔ Custom | ⛔             | ⛔             |
| [Google Gemma 1.1 7b](https://huggingface.co/google/gemma-1.1-7b-it) | ⛔ Custom | ⛔             | ⛔             |
| [Alibaba Qwen 1.5 7b](https://huggingface.co/Qwen/Qwen1.5-7B)        | ⛔ Custom | ⛔             | ⛔             |

---

# LLMs with Openly Licensed Datasets

- [Allan AI OLMo](https://huggingface.co/allenai/OLMo-7B) based on the [Dolma dataset](https://huggingface.co/datasets/allenai/dolma)
- [LumiOpen Viking](https://huggingface.co/LumiOpen/Viking-7B) built on [Lumi Supercomputer](https://www.lumi-supercomputer.eu/)
- [HuggingFace StarChat2](https://huggingface.co/HuggingFaceH4/starchat2-15b-v0.1) focussed on code
- [OpenGPT-X](https://opengpt-x.de/en/project/) EU funded

---

# LLM Inference Implementation

Generate a text based on a prompt

```python
import ollama

res = ollama.chat(
    model="zephyr:7b-beta",
    messages=[{"role": "user", "content": f"Summarize this text: {text}"}],
    stream=False,
)
res["message"]["content"] # "The given text..."
```
<!-- footer: "More code: https://github.com/rti/barebone-rag/blob/main/models.py" -->

---

# Conclusion

- ✅ Almost all components are available with OSI approved licenses
- ✅ Different hardware platforms supported
- ⏳ Fully Open Source LLMs are not really there yet
- 🙏 Interesting developments ongoing

<!-- footer: "" -->
