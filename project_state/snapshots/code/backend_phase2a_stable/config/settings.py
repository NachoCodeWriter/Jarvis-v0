# ============================================
# IMPORTS
# ============================================

from pathlib import Path


# ============================================
# BASE PATHS
# ============================================

BASE_DIR: Path = Path("/home/jarvis/jarvis")

BACKEND_DIR: Path = BASE_DIR / "backend"

DATA_DIR: Path = BASE_DIR / "data"

LOG_DIR: Path = BASE_DIR / "logs"

RAG_DIR: Path = BASE_DIR / "rag"

RAG_INPUT_DIR: Path = RAG_DIR / "input"

RAG_PROCESSED_DIR: Path = RAG_DIR / "processed"

BACKUP_DIR: Path = BASE_DIR / "backups"

MEMORY_DIR: Path = BACKEND_DIR / "memory"

MEMORY_DB_PATH: Path = MEMORY_DIR / "jarvis_memory.db"


# ============================================
# MODEL CONFIGURATION
# ============================================

MODEL_NAME: str = "qwen2.5:7b"

TEMPERATURE: float = 0.5

MAX_CONTEXT_CHARS: int = 12000

MAX_TOOL_RESPONSE_CHARS: int = 4000


# ============================================
# MEMORY CONFIGURATION
# ============================================

MEMORY_LIMIT: int = 10

MAX_MEMORY_MESSAGES: int = 50


# ============================================
# FILE LIMITS
# ============================================

MAX_FILE_READ_CHARS: int = 5000

MAX_PROMPT_CHARS: int = 8000


# ============================================
# SECURITY CONFIGURATION
# ============================================

ALLOW_SYSTEM_COMMANDS: bool = False

ALLOW_INTERNET_ACCESS: bool = False

SAFE_MODE: bool = True


# ============================================
# AUTONOMY CONFIGURATION
# ============================================

AUTONOMOUS_MODE: bool = False

REQUIRE_TOOL_CONFIRMATION: bool = True


# ============================================
# RAG CONFIGURATION
# ============================================

EMBEDDING_MODEL: str = "intfloat/multilingual-e5-small"

RAG_TOP_K: int = 3

RAG_CHUNK_SIZE: int = 500

RAG_CHUNK_OVERLAP: int = 50


# ============================================
# SEMANTIC MEMORY CONFIGURATION
# ============================================

SEMANTIC_MEMORY_COLLECTION: str = "jarvis_memory"

SEMANTIC_TOP_K: int = 5

MAX_EMBED_TEXT_CHARS: int = 1500

DEFAULT_MEMORY_IMPORTANCE: float = 0.5


# ============================================
# LOGGING CONFIGURATION
# ============================================

LOG_LEVEL: str = "INFO"


# ============================================
# SYSTEM PROMPT
# ============================================

SYSTEM_PROMPT: str = """
Eres Jarvis, un agente autónomo profesional avanzado.

Tu función es:

- asistir al usuario
- razonar cuidadosamente
- utilizar herramientas cuando sea necesario
- mantener contexto conversacional
- responder de forma clara y precisa

Nunca inventes información.

Si no sabes algo:

- dilo claramente
- explica la limitación
- propone cómo obtener la información

No inventes intereses, objetivos o intenciones
que el usuario no haya mencionado.

Responde en español salvo que el usuario
indique lo contrario.
"""
