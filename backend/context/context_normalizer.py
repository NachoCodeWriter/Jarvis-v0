from backend.utils.logger import (
    memory_logger
)

# =========================================
# TEXT NORMALIZER
# =========================================

def normalize_text(
    text: str
) -> str:

    return (
        text.strip()
        .lower()
        .replace("\n", " ")
    )

# =========================================
# DEDUPLICATION
# =========================================

def deduplicate_messages(
    messages: list
) -> list:

    seen_messages = set()

    unique_messages = []

    for message in messages:

        role = message.get(
            "role",
            ""
        )

        content = message.get(
            "content",
            ""
        )

        normalized = normalize_text(
            f"{role}:{content}"
        )

        if normalized in seen_messages:
            continue

        seen_messages.add(
            normalized
        )

        unique_messages.append(
            message
        )

    memory_logger.info(
        f"""
CONTEXT NORMALIZATION COMPLETE

Original Messages:
{len(messages)}

Unique Messages:
{len(unique_messages)}
"""
    )

    return unique_messages
