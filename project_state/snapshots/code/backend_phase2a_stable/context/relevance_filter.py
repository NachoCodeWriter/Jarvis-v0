import re


from backend.utils.logger import (
    memory_logger
)

# =========================================
# RELEVANCE FILTER
# =========================================

MIN_RELEVANCE_SCORE = 1


def tokenize(
    text: str
) -> set:

    normalized_text = re.sub(
    r"[^\w\s]",
    "",
    text.lower()
)

    return set(
    word
    for word in normalized_text.split()
    if len(word) > 2
)


def calculate_relevance(
    prompt: str,
    content: str
) -> int:

    prompt_tokens = tokenize(prompt)
    content_tokens = tokenize(content)

    overlap = prompt_tokens.intersection(
        content_tokens
    )

    return len(overlap)


def filter_relevant_messages(
    user_prompt: str,
    messages: list
) -> list:

    relevant_messages = []

    keep_next_assistant = False

    for message in messages:

        role = message.get(
            "role",
            ""
        )

        content = message.get(
            "content",
            ""
        )

        # ------------------------------
        # KEEP ASSISTANT AFTER RELEVANT USER
        # ------------------------------

        if (
            role == "assistant"
            and keep_next_assistant
        ):

            relevant_messages.append(
                message
            )

            keep_next_assistant = False

            continue

        # ------------------------------
        # USER RELEVANCE SCORING
        # ------------------------------

        score = calculate_relevance(
            user_prompt,
            content
        )

        if score >= MIN_RELEVANCE_SCORE:

            relevant_messages.append(
                message
            )

            if role == "user":
                keep_next_assistant = True

    memory_logger.info(
        f"Mensajes relevantes filtrados: {len(relevant_messages)}"
    )

    return relevant_messages
