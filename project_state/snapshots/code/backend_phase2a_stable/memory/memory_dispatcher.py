from backend.memory.semantic_memory import (
    index_memory
)

from backend.utils.logger import (
    memory_logger,
    error_logger
)


# =========================================
# MEMORY EVENT DISPATCHER
# =========================================

def dispatch_memory_event(
    memory_id: int,
    role: str,
    content: str,
    timestamp: str
) -> bool:

    try:

        memory_logger.info(
            f"Dispatching memory event: {memory_id}"
        )

        result = index_memory(
            memory_id=memory_id,
            role=role,
            content=content,
            timestamp=timestamp
        )

        if result:

            memory_logger.info(
                f"Memory event completed: {memory_id}"
            )

        else:

            memory_logger.warning(
                f"Memory event failed: {memory_id}"
            )

        return result

    except Exception as error:

        error_logger.error(
            f"Memory dispatcher error: {error}"
        )

        return False
