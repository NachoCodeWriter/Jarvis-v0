# PROJECT STATE

## CURRENT STATUS

Jarvis backend functional.

Implemented:
- conversational memory
- persistent memory
- relevance filtering
- assistant memory sanitizer
- tool payload filtering
- context builder
- intent routing
- tool execution pipeline
- RAG search
- semantic normalization

## CURRENT STACK

- FastAPI
- Ollama
- sentence-transformers
- chromadb
- torch
- transformers

## ACTIVE MODELS

### LLM
- qwen2.5:7b

### EMBEDDINGS
- nomic-embed-text

## MEMORY STATUS

Current memory system:
- token overlap relevance
- punctuation normalization
- assistant response sanitization

Pending:
- real semantic embeddings
- vector memory
- semantic retrieval
- semantic ranking

## ARCHITECTURE STYLE

- modular
- lightweight
- local-first
- framework-minimal
- explicit orchestration
- highly inspectable

## HARDWARE PROFILE

### CPU
- Intel i7-9700K

### RAM
- 24GB allocated to WSL

### GPU
- RTX 2060 6GB VRAM

### STORAGE
- Dedicated SSD A: 446GB

## DESIGN PHILOSOPHY

- no heavy abstractions
- no opaque agent frameworks
- maximum inspectability
- surgical incremental development
- production-oriented architecture

## CURRENT PHASE

Transitioning from:
- lexical relevance memory

Towards:
- semantic vector memory architecture
