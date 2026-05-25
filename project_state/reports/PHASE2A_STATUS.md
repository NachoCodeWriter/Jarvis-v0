# JARVIS — PHASE 2A COMPLETE

## Estado general

Jarvis dispone ahora de:

- memoria persistente SQLite
- memoria semántica vectorial
- retrieval híbrido
- ranking auxiliar
- dispatcher desacoplado
- sanitización de memoria
- graceful degradation
- contexto semántico dinámico

---

# Arquitectura actual

Usuario
↓
SQLite persistence
↓
Memory Dispatcher
↓
Semantic Indexing (ChromaDB)
↓
Semantic Retrieval
↓
Memory Ranking
↓
Context Builder
↓
LLM
↓
Assistant Response
↓
Memory Persistence + Reindex

---

# Modelos

LLM:
- qwen2.5:7b

Embedding model:
- intfloat/multilingual-e5-small

---

# Stack

- FastAPI
- SQLite
- ChromaDB
- SentenceTransformers
- Ollama
- Python 3.14

---

# Decisiones arquitectónicas importantes

## Retrieval position

Retrieval ocurre:
- después del intent router
- antes del LLM

---

## Semantic ranking

El relevance_filter clásico:
- NO es el filtro principal
- ES señal auxiliar de ranking

---

## Memory indexing

Indexación:
- desacoplada mediante dispatcher
- actualmente síncrona
- preparada para futura asincronía

---

## Memory IDs

SQLite AUTOINCREMENT:
- es la source of truth

---

# Estado actual

Sistema estable.

Tests validados:
- retrieval semántico
- persistencia
- ranking
- reconstrucción de contexto
- recuperación cross-session

---

# Próxima fase

PHASE 2B:
Memory Importance System
