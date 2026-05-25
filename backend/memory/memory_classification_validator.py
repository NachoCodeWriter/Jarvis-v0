# =========================================
# VALID MEMORY TYPES
# =========================================

VALID_MEMORY_TYPES = {
    "episodic",
    "semantic",
    "preference",
    "project",
    "goal",
    "procedural",
    "relational",
    "reflective"
}

# =========================================
# DEFAULT CLASSIFICATION
# =========================================

DEFAULT_CLASSIFICATION = {
    "memory_types": [],
    "importance": 0.0,
    "confidence": 0.0,
    "should_index": False,
    "should_profile": False,
    "should_consolidate": False,
    "tags": [],
    "inferred_facts": [],
    "reasoning": ""
}

# =========================================
# FLOAT NORMALIZER
# =========================================

def normalize_float(
    value,
    default=0.0
) -> float:

    try:

        value = float(value)

        if value < 0.0:
            return 0.0

        if value > 1.0:
            return 1.0

        return value

    except Exception:
        return default

# =========================================
# BOOLEAN NORMALIZER
# =========================================

def normalize_bool(
    value
) -> bool:

    return bool(value)

# =========================================
# LIST NORMALIZER
# =========================================

def normalize_list(
    value
) -> list:

    if isinstance(value, list):
        return value

    return []

# =========================================
# MEMORY TYPE NORMALIZER
# =========================================

def normalize_memory_types(
    memory_types
) -> list:

    normalized = []

    for memory_type in normalize_list(
        memory_types
    ):

        if not isinstance(
            memory_type,
            str
        ):
            continue

        memory_type = memory_type.strip().lower()

        if memory_type in VALID_MEMORY_TYPES:

            normalized.append(
                memory_type
            )

    return list(
        set(normalized)
    )

# =========================================
# CLASSIFICATION VALIDATOR
# =========================================

def validate_classification(
    classification: dict
) -> dict:

    validated = DEFAULT_CLASSIFICATION.copy()

    validated["memory_types"] = (
        normalize_memory_types(
            classification.get(
                "memory_types",
                []
            )
        )
    )

    validated["importance"] = (
        normalize_float(
            classification.get(
                "importance",
                0.0
            )
        )
    )

    validated["confidence"] = (
        normalize_float(
            classification.get(
                "confidence",
                0.0
            )
        )
    )

    validated["should_index"] = (
        normalize_bool(
            classification.get(
                "should_index",
                False
            )
        )
    )

    validated["should_profile"] = (
        normalize_bool(
            classification.get(
                "should_profile",
                False
            )
        )
    )

    validated["should_consolidate"] = (
        normalize_bool(
            classification.get(
                "should_consolidate",
                False
            )
        )
    )

    validated["tags"] = (
        normalize_list(
            classification.get(
                "tags",
                []
            )
        )
    )

    validated["inferred_facts"] = (
        normalize_list(
            classification.get(
                "inferred_facts",
                []
            )
        )
    )

    reasoning = classification.get(
        "reasoning",
        ""
    )

    validated["reasoning"] = str(
        reasoning
    )

    return validated
