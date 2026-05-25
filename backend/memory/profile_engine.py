import json

from pathlib import Path

from backend.utils.logger import (
    memory_logger,
    error_logger
)

# =========================================
# PROFILE STORAGE
# =========================================

PROFILE_PATH = Path(
    "~/jarvis/data/profiles/default_user.json"
).expanduser()

# =========================================
# LOAD PROFILE
# =========================================

def load_profile() -> dict:

    try:

        if not PROFILE_PATH.exists():

            return {
                "traits": {},
                "preferences": {},
                "projects": {},
                "goals": {},
                "tags": [],
                "metadata": {}
            }

        with open(
            PROFILE_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception as error:

        error_logger.error(
            f"Error loading profile: {error}"
        )

        return {}

# =========================================
# SAVE PROFILE
# =========================================

def save_profile(
    profile: dict
) -> bool:

    try:

        PROFILE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            PROFILE_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                profile,
                file,
                indent=4,
                ensure_ascii=False
            )

        memory_logger.info(
            "Profile saved successfully"
        )

        return True

    except Exception as error:

        error_logger.error(
            f"Error saving profile: {error}"
        )

        return False

# =========================================
# UPDATE PROFILE FIELD
# =========================================

def update_profile_field(
    category: str,
    key: str,
    value,
    confidence: float = 0.5
) -> bool:

    try:

        profile = load_profile()

        if category not in profile:

            profile[category] = {}

        existing = profile[
            category
        ].get(key)

        # ---------------------------------
        # MERGE STRATEGY
        # ---------------------------------

        if existing:

            old_confidence = existing.get(
                "confidence",
                0.5
            )

            confidence = max(
                confidence,
                old_confidence
            )

        profile[category][key] = {
            "value": value,
            "confidence": confidence
        }

        save_profile(
            profile
        )

        memory_logger.info(
            f"""
PROFILE UPDATED

Category:
{category}

Key:
{key}

Confidence:
{confidence}
"""
        )

        return True

    except Exception as error:

        error_logger.error(
            f"Error updating profile: {error}"
        )

        return False

# =========================================
# ADD PROFILE TAGS
# =========================================

def add_profile_tags(
    tags: list
) -> bool:

    try:

        profile = load_profile()

        existing_tags = set(
            profile.get(
                "tags",
                []
            )
        )

        existing_tags.update(
            tags
        )

        profile["tags"] = list(
            existing_tags
        )

        save_profile(
            profile
        )

        return True

    except Exception as error:

        error_logger.error(
            f"Error adding profile tags: {error}"
        )

        return False
