---
title:
  - Semantic Search and RAG on a FOSS stack
author:
  - Robert Timm
---

# Semantic Search and RAG on a FOSS stack

Robert Timm
<robert.timm@wikimedia.de>

Wikimedia Hackathon 2024 Tallinn

---

---

# LLMs with Openly Licensed Weights

| Model Name                                                                             | License         | Pre Train Data | Fine Tune Data |
| -------------------------------------------------------------------------------------- | --------------- | -------------- | -------------- |
| [Mistral 0.2 7b](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)            | ✅ Apache-2.0   | ⛔             | ⛔             |
| [HF Zephyr 7b beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)               | ✅ MIT          | ⛔             | ✅             |
| [OpenChat 7b 3.5](https://huggingface.co/openchat/openchat-3.5-0106)                   | ✅ Apache-2.0   | ⛔             | ✅             |
| [Cohere Command-R 35b](https://huggingface.co/CohereForAI/c4ai-command-r-v01)          | ✅ CC-BY-NC 4.0 | ⛔             | ⛔             |
| [Stability.AI StableLM2 1.6b](https://huggingface.co/stabilityai/stablelm-2-1_6b-chat) | ⛔ Custom       | ✅             | ✅             |
| [Olmo](https://huggingface.co/allenai/OLMo-7B) | | |

---

# Other Famous LLMs

| Model Name                                                           | License   | Pre Train Data | Fine Tune Data |
| -------------------------------------------------------------------- | --------- | -------------- | -------------- |
| [Meta Llama 3 8b](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | ⛔ Custom | ⛔             | ⛔             |
| [Google Gemma 1.1 7b](https://huggingface.co/google/gemma-1.1-7b-it) | ⛔ Custom | ⛔             | ⛔             |
| [Alibaba Qwen 1.5 7b](https://huggingface.co/Qwen/Qwen1.5-7B)        | ⛔ Custom | ⛔             | ⛔             |

---

# Notable LLMs with Open Weights Licenses

---

| Model Name                                                                        | License    | Training Data | Fine Tuning Data |
| --------------------------------------------------------------------------------- | ---------- | ------------- | ---------------- |
| [all-MiniLM L6 V2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | apache-2.0 | Yes           | Available        |
| [Nomic Embed](https://blog.nomic.ai/posts/nomic-embed-text-v1)                    | apache-2.0 | Yes           | Available        |
| [mxbai-embed-large-v1](https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1) | apache-2.0 | No            | Unknown          |
