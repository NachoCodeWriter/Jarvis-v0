import logging
import os

from backend.config.settings import LOG_DIR


# =========================================
# CREATE LOG DIRECTORY
# =========================================

os.makedirs(LOG_DIR, exist_ok=True)


# =========================================
# LOGGER FACTORY
# =========================================

def create_logger(name: str, filename: str):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s"
    )

    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, filename)
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)

    return logger


# =========================================
# SYSTEM LOGGER
# =========================================

system_logger = create_logger(
    "system_logger",
    "system.log"
)


# =========================================
# ERROR LOGGER
# =========================================

error_logger = create_logger(
    "error_logger",
    "errors.log"
)


# =========================================
# LLM LOGGER
# =========================================

llm_logger = create_logger(
    "llm_logger",
    "llm.log"
)


# =========================================
# TOOL LOGGER
# =========================================

tool_logger = create_logger(
    "tool_logger",
    "tools.log"
)


# =========================================
# MEMORY LOGGER
# =========================================

memory_logger = create_logger(
    "memory_logger",
    "memory.log"
)


# =========================================
# RAG LOGGER
# =========================================

rag_logger = create_logger(
    "rag_logger",
    "rag.log"
)
