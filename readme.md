## Quickstart

```
docker compose up --build
```

```
docker compose run --build app import_dump.py
```

### LLMs with open weights licenses

#### Mistral 0.2 7b by Mistral AI (apache-2.0)

- https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2
- Training data NOT available

#### Zephyr 7b beta by HugginFace (MIT)

- https://huggingface.co/HuggingFaceH4/zephyr-7b-beta
- based on Mistral 0.1 7b
- Code, model, data and tutorials publicly available

#### OpenChat 7b 3.5 0106 by Tsinghua University et al. (apache-2.0)

- https://huggingface.co/openchat/openchat-3.5-0106
- based on Mistral 0.1 7b
- Code, model and data publically available

#### Command R 35b by Cohere For AI (CC-BY-NC 4.0)

- https://huggingface.co/CohereForAI/c4ai-command-r-v01
- Training data NOT available
- Focus on RAG, supports function calling
- 128k context

#### StarChat2 15b by HuggingFace and BigCode (BigCode Open RAIL-M v1)

- https://huggingface.co/HuggingFaceH4/starchat2-15b-v0.1
- https://huggingface.co/spaces/bigcode/bigcode-model-license-agreement
- based on StarCoder2 https://huggingface.co/bigcode/starcoder2-15b
- training data available

#### Gemma 1.1 7b by Google Brain (gemma license)

- https://huggingface.co/google/gemma-1.1-7b-it
- https://ai.google.dev/gemma/terms
- https://ai.google.dev/gemma/prohibited_use_policy
- Training data NOT available
- Restrictions on use cases to not cause any harm 

#### Llama 3 8b by Meta/Facebook (llama 3 license)

- https://huggingface.co/meta-llama/Meta-Llama-3-8B
- https://llama.meta.com/llama3/license/
- Training data NOT available
- Deriviates must have the same license
- Restriction on using output for other models
- Extra license for >700M active users / month

#### Qwen 1.5 7B by Alibaba Cloud (qwen license)

- https://huggingface.co/Qwen/Qwen1.5-7B
- https://huggingface.co/Qwen/Qwen1.5-7B-Chat-GGUF/blob/main/LICENSE
- Training data NOT available
- Must not be used to improve other models
- Extra license for >100M active users / month


### Embedding models with open weights licenses

https://huggingface.co/spaces/mteb/leaderboard

#### all-MiniLM L6 V2 by Microsoft + SBert (apache-2.0)

- https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- 384 dimensions
- 33M parameters
- Training data available

#### Nomic Embed by Nomic AI (apache-2.0)

- https://blog.nomic.ai/posts/nomic-embed-text-v1
- 768 dimensions
- 137M parameters
- Open source, Open data, Open training code, Fully reproducible and auditable

#### mxbai-embed-large-v1 by mixedbread.ai (apache-2.0)

- https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1
- 1024 dimensions
- 335M parameters
- Training data NOT available

