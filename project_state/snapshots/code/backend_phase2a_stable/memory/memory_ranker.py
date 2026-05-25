import re


# =========================================
# RANKING WEIGHTS
# =========================================

SEMANTIC_WEIGHT = 0.8

LEXICAL_WEIGHT = 0.2


# =========================================
# TOKENIZATION
# =========================================

def tokenize(
    text: str
) -> set:

    normalized = re.sub(
        r"[^\w\s]",
        "",
        text.lower()
    )

    return {
        token
        for token in normalized.split()
        if len(token) > 2
    }


# =========================================
# LEXICAL OVERLAP
# =========================================

def calculate_lexical_overlap(
    query: str,
    content: str
) -> float:

    query_tokens = tokenize(query)

    content_tokens = tokenize(content)

    overlap = query_tokens.intersection(
        content_tokens
    )

    if not query_tokens:
        return 0.0

    return len(overlap) / len(query_tokens)


# =========================================
# SEMANTIC SCORE
# =========================================

def normalize_semantic_score(
    distance: float
) -> float:

    return max(
        0.0,
        1.0 - distance
    )


# =========================================
# HYBRID SCORE
# =========================================

def calculate_hybrid_score(
    query: str,
    memory: dict
) -> float:

    content = memory.get(
        "content",
        ""
    )

    semantic_distance = memory.get(
        "score",
        1.0
    )

    semantic_score = normalize_semantic_score(
        semantic_distance
    )

    lexical_score = calculate_lexical_overlap(
        query,
        content
    )

    hybrid_score = (
        semantic_score * SEMANTIC_WEIGHT
        +
        lexical_score * LEXICAL_WEIGHT
    )

    return hybrid_score


# =========================================
# MEMORY RANKING
# =========================================

def rank_memories(
    query: str,
    memories: list
) -> list:

    ranked_memories = []

    for memory in memories:

        hybrid_score = calculate_hybrid_score(
            query,
            memory
        )

        enriched_memory = {
            **memory,
            "hybrid_score": hybrid_score
        }

        ranked_memories.append(
            enriched_memory
        )

    ranked_memories.sort(
        key=lambda memory:
        memory["hybrid_score"],
        reverse=True
    )

    return ranked_memories
