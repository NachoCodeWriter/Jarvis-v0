# JARVIS ARCHITECTURE

## OVERVIEW

Jarvis is a modular local-first AI assistant architecture designed for:

- persistent conversational memory
- semantic retrieval
- RAG pipelines
- multitool orchestration
- inspectable reasoning pipelines
- lightweight local execution

The system prioritizes:

- modularity
- transparency
- low VRAM usage
- incremental extensibility
- explicit orchestration

---

# CORE PRINCIPLES

## 1. LOCAL-FIRST

Primary execution occurs locally.

Avoid:
- external APIs
- cloud dependency
- opaque hosted orchestration

---

## 2. MODULAR ARCHITECTURE

Each subsystem must remain isolated and replaceable.

Examples:
- memory layer
- embedding layer
- retrieval layer
- orchestration layer
- tool layer

must evolve independently.

---

## 3. EXPLICIT PIPELINES

Avoid hidden framework abstractions.

All major flows should remain:
- readable
- inspectable
- debuggable

---

## 4. LOW VRAM OPTIMIZATION

Architecture targets:
- RTX 2060 6GB
- efficient inference
- lightweight embeddings
- controlled context growth

---

# CURRENT ARCHITECTURE

## ENTRYPOINT

FastAPI backend.

Primary route:
- /agent/chat

---

## MAIN FLOW

User Prompt
→ Intent Detection
→ Context Builder
→ Memory Retrieval
→ Tool Routing
→ LLM Call
→ Sanitization
→ Persistent Memory Save

---

# MEMORY SYSTEM

## CURRENT MEMORY

Current memory uses:
- lexical relevance overlap
- punctuation normalization
- assistant contamination sanitization

---

## FUTURE MEMORY

Planned migration:
- semantic embeddings
- vector similarity retrieval
- semantic ranking
- memory scoring
- memory decay systems

---

# EMBEDDING STRATEGY

## CURRENT

Installed:
- nomic-embed-text

Planned:
- semantic conversational embeddings
- vector memory retrieval

---

# LLM LAYER

## ACTIVE MODEL

qwen2.5:7b

Served through:
- Ollama

---

# STORAGE STRATEGY

## CURRENT

Persistent conversational memory stored locally.

## FUTURE

Planned:
- ChromaDB vector persistence
- semantic indexing
- retrieval metadata
- hybrid retrieval

---

# TOOL SYSTEM

Current tools:
- RAG search
- file search pipeline
- routing layer
- tool execution layer

Architecture prepared for:
- browser tools
- OCR
- Whisper
- TTS
- planners
- agent workflows

---

# CONTEXT MANAGEMENT

Current protections:
- tool payload filtering
- assistant sanitizer
- relevance filtering
- context truncation

Future goals:
- semantic context ranking
- dynamic context windows
- importance scoring

---

# DEVELOPMENT STYLE

Development follows:
- surgical incremental changes
- snapshot-based recovery
- state freezing before major transitions
- architecture-first evolution

No uncontrolled rewrites allowed.

---

# CURRENT TRANSITION PHASE

Jarvis is currently transitioning from:

LEXICAL MEMORY SYSTEM

towards:

SEMANTIC VECTOR MEMORY ARCHITECTURE
