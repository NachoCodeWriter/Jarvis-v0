from backend.config.settings import (
    MEMORY_LIMIT,
    MAX_CONTEXT_CHARS,
    MAX_TOOL_RESPONSE_CHARS
)

from backend.memory.persistent_memory import (
    get_recent_messages
)

from backend.context.relevance_filter import (
    filter_relevant_messages
)

from backend.context.context_normalizer import (
    deduplicate_messages
)

from backend.memory.semantic_memory import (
    retrieve_semantic_memories
)

from backend.memory.memory_ranker import (
    rank_memories
)

from backend.utils.logger import (
    memory_logger,
    error_logger
)

# =========================================
# TOOL MESSAGE DETECTION
# =========================================

TOOL_PATTERNS = [
    "'tool':",
    '"tool":',
    "'results':",
    '"results":',
    "'documents':",
    '"documents":'
]

# =========================================
# TOOL MESSAGE FILTER
# =========================================

def is_tool_message(
    message: dict
) -> bool:

    content = str(
        message.get("content", "")
    )

    return any(
        pattern in content
        for pattern in TOOL_PATTERNS
    )

# =========================================
# TEXT TRUNCATOR
# =========================================

def truncate_text(
    text: str,
    limit: int
) -> str:

    if len(text) <= limit:
        return text

    return (
        text[:limit]
        + "\n...[TRUNCATED]"
    )

# =========================================
# MEMORY CLEANER
# =========================================

def clean_memory_messages(
    messages: list
) -> list:

    cleaned_messages = []

    for message in messages:

        role = message.get("role", "")
        content = str(
            message.get("content", "")
        ).strip()

        # ---------------------------------
        # SKIP EMPTY
        # ---------------------------------

        if not content:
            continue

        # ---------------------------------
        # REMOVE TOOL PAYLOADS
        # ---------------------------------

        if is_tool_message(message):

            cleaned_messages.append({
                "role": "system",
                "content": "[Tool execution omitted from conversational memory]"
            })

            continue

        # ---------------------------------
        # TRUNCATE LONG MESSAGES
        # ---------------------------------

        content = truncate_text(
            content,
            MAX_TOOL_RESPONSE_CHARS
        )

        cleaned_messages.append({
            "role": role,
            "content": content
        })

    return cleaned_messages

# =========================================
# CONTEXT BUILDER
# =========================================

def build_context(
    user_prompt: str
) -> str:

    try:

        memory_messages = get_recent_messages(
            limit=MEMORY_LIMIT
        )

        cleaned_messages = clean_memory_messages(
            memory_messages
        )

        semantic_memories = retrieve_semantic_memories(
            query=user_prompt,
            top_k=5
        )

        if semantic_memories:

            ranked_memories = rank_memories(
                query=user_prompt,
                memories=semantic_memories
            )

            relevant_messages = []

            for memory in ranked_memories:

                relevant_messages.append({
                    "role": memory["metadata"].get(
                        "role",
                        "user"
                    ),
                    "content": memory["content"]
                })

        else:

            relevant_messages = filter_relevant_messages(
                user_prompt,
                cleaned_messages
            )

        relevant_messages = (
            deduplicate_messages(
                relevant_messages
            )
        )

        conversation_lines = []

        for message in relevant_messages:

            role = message["role"]
            content = message["content"]

            conversation_lines.append(
                f"{role}: {content}"
            )

        conversation_text = "\n".join(
            conversation_lines
        )

        final_context = f"""
Conversación previa:

{conversation_text}

Usuario:
{user_prompt}

Responde de forma natural, útil y breve.
"""

        final_context = truncate_text(
            final_context,
            MAX_CONTEXT_CHARS
        )

        # ---------------------------------
        # COMPACT LOGGING
        # ---------------------------------

        memory_logger.info(
            f"""
CHAT CONTEXT GENERATED

User Prompt:
{user_prompt}

Messages Used:
{len(relevant_messages)}

Context Length:
{len(final_context)}
"""
        )

        return final_context

    except Exception as error:

        error_logger.error(
            f"Error construyendo contexto: {error}"
        )

        return user_prompt
