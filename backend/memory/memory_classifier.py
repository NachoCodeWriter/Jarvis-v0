import json

import ollama

from backend.config.settings import (
    CLASSIFIER_MODEL,
    CLASSIFIER_TEMPERATURE,
    CLASSIFIER_MAX_TOKENS,
    CLASSIFIER_TIMEOUT
)

from backend.memory.classification_prompts import (
    MEMORY_CLASSIFIER_SYSTEM_PROMPT
)

from backend.memory.memory_classification_validator import (
    validate_classification
)

from backend.utils.logger import (
    memory_logger,
    error_logger
)

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
# MEMORY CLASSIFIER
# =========================================

def classify_memory(
    role: str,
    content: str
) -> dict:

    try:

        memory_logger.info(
            f"Classifying memory | role={role}"
        )

        user_prompt = f"""
Role:
{role}

Content:
{content}
"""

        response = ollama.chat(
            model=CLASSIFIER_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": MEMORY_CLASSIFIER_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            options={
                "temperature": CLASSIFIER_TEMPERATURE,
                "num_predict": CLASSIFIER_MAX_TOKENS
            }
        )

        raw_content = response["message"]["content"]

        classification = json.loads(
            raw_content
        )

        classification = validate_classification(
            classification
        )

        memory_logger.info(
            f"""
MEMORY CLASSIFICATION COMPLETE

Types:
{classification.get("memory_types")}

Importance:
{classification.get("importance")}

Confidence:
{classification.get("confidence")}
"""
        )

        return classification

    except Exception as error:

        error_logger.error(
            f"Error classifying memory: {error}"
        )

        return DEFAULT_CLASSIFICATION.copy()
