from backend.memory.memory_classifier import (
    classify_memory
)

from backend.memory.profile_extractor import (
    extract_profile_updates,
    apply_profile_updates
)

from backend.utils.logger import (
    memory_logger,
    error_logger
)

# =========================================
# COGNITIVE PIPELINE
# =========================================

def process_cognitive_memory(
    role: str,
    content: str
) -> dict:

    try:

        memory_logger.info(
            f"""
COGNITIVE PIPELINE START

Role:
{role}
"""
        )

        # ---------------------------------
        # CLASSIFICATION
        # ---------------------------------

        classification = classify_memory(
            role=role,
            content=content
        )

        profile_updates = (
            extract_profile_updates(
                classification
            )
        )

        apply_profile_updates(
            profile_updates
        )

        # ---------------------------------
        # MEMORY ACTIONS
        # ---------------------------------

        memory_actions = {
            "should_index": classification.get(
                "should_index",
                False
            ),

            "should_profile": classification.get(
                "should_profile",
                False
            ),

            "should_consolidate": classification.get(
                "should_consolidate",
                False
            )
        }

        # ---------------------------------
        # PIPELINE RESULT
        # ---------------------------------

        pipeline_result = {

            "classification": classification,

            "memory_actions": memory_actions,

            "profile_updates": [],

            "consolidation_candidates": []
        }

        memory_logger.info(
            f"""
COGNITIVE PIPELINE COMPLETE

Types:
{classification.get("memory_types")}

Importance:
{classification.get("importance")}
"""
        )

        return pipeline_result

    except Exception as error:

        error_logger.error(
            f"Error in cognitive pipeline: {error}"
        )

        return {
            "classification": {},
            "memory_actions": {},
            "profile_updates": [],
            "consolidation_candidates": []
        }
