from backend.config.settings import (
    PROFILE_MIN_CONFIDENCE
)

from backend.memory.profile_engine import (
    update_profile_field,
    add_profile_tags
)

from backend.utils.logger import (
    memory_logger,
    error_logger
)

# =========================================
# PROFILE EXTRACTION
# =========================================

def extract_profile_updates(
    classification: dict
) -> dict:

    try:

        updates = {
            "preferences": [],
            "projects": [],
            "goals": [],
            "traits": [],
            "tags": []
        }

        confidence = classification.get(
            "confidence",
            0.0
        )

        if confidence < PROFILE_MIN_CONFIDENCE:

            return updates

        # ---------------------------------
        # MEMORY TYPES
        # ---------------------------------

        memory_types = classification.get(
            "memory_types",
            []
        )

        tags = classification.get(
            "tags",
            []
        )

        reasoning = classification.get(
            "reasoning",
            ""
        )

        # ---------------------------------
        # PROJECT DETECTION
        # ---------------------------------

        if "project" in memory_types:

            for tag in tags:

                updates["projects"].append({
                    "key": tag,
                    "value": True,
                    "confidence": confidence
                })

        # ---------------------------------
        # GOAL DETECTION
        # ---------------------------------

        if "goal" in memory_types:

            for tag in tags:

                updates["goals"].append({
                    "key": tag,
                    "value": True,
                    "confidence": confidence
                })

        # ---------------------------------
        # TAG STORAGE
        # ---------------------------------

        updates["tags"] = tags

        memory_logger.info(
            f"""
PROFILE EXTRACTION COMPLETE

Projects:
{len(updates["projects"])}

Goals:
{len(updates["goals"])}

Tags:
{len(tags)}
"""
        )

        return updates

    except Exception as error:

        error_logger.error(
            f"Error extracting profile updates: {error}"
        )

        return {}

# =========================================
# APPLY PROFILE UPDATES
# =========================================

def apply_profile_updates(
    updates: dict
) -> bool:

    try:

        # ---------------------------------
        # PROJECTS
        # ---------------------------------

        for item in updates.get(
            "projects",
            []
        ):

            update_profile_field(
                category="projects",
                key=item["key"],
                value=item["value"],
                confidence=item["confidence"]
            )

        # ---------------------------------
        # GOALS
        # ---------------------------------

        for item in updates.get(
            "goals",
            []
        ):

            update_profile_field(
                category="goals",
                key=item["key"],
                value=item["value"],
                confidence=item["confidence"]
            )

        # ---------------------------------
        # TAGS
        # ---------------------------------

        add_profile_tags(
            updates.get(
                "tags",
                []
            )
        )

        memory_logger.info(
            """
PROFILE UPDATE PIPELINE COMPLETE
"""
        )

        return True

    except Exception as error:

        error_logger.error(
            f"Error applying profile updates: {error}"
        )

        return False
