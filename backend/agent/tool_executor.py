from backend.tools.file_search import search_files
from backend.tools.file_read import read_file
from backend.tools.rag_search import rag_search

from backend.config.settings import (
    BASE_DIR,
    MAX_FILE_READ_CHARS
)


# ============================================
# FILE SEARCH TOOL
# ============================================

def execute_file_search(prompt: str) -> dict:

    results = search_files(BASE_DIR, prompt)

    return {
        "tool": "file_search",
        "results": results
    }


# ============================================
# FILE READ TOOL
# ============================================

def execute_file_read(prompt: str) -> dict:

    path = (
        prompt
        .replace("lee archivo", "")
        .replace("abre archivo", "")
        .replace("leer archivo", "")
        .strip()
    )

    content = read_file(path)

    return {
        "tool": "file_read",
        "content": content[:MAX_FILE_READ_CHARS]
    }


# ============================================
# RAG SEARCH TOOL
# ============================================

def execute_rag(prompt: str) -> dict:

    documents = rag_search(prompt)

    return {
        "tool": "rag_search",
        "documents": documents
    }


# ============================================
# TOOL REGISTRY
# ============================================

TOOLS = {
    "file_search": execute_file_search,
    "file_read": execute_file_read,
    "rag": execute_rag
}


# ============================================
# TOOL EXECUTOR
# ============================================

def execute_tool(intent: str, prompt: str):

    tool_function = TOOLS.get(intent)

    if tool_function is None:
        return None

    return tool_function(prompt)
