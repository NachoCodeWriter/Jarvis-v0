import re


# =====================================
# CONTAMINATION PATTERNS
# =====================================

CONTAMINATION_PATTERNS = [

    r"si necesitas un pdf.*",
    r"si buscas un pdf.*",
    r"si buscas un documento.*",
    r"puedo ayudarte a encontrar.*",
    r"estoy aqui para ayudarte.*",
    r"estoy aquí para ayudarte.*",
    r"si necesitas más información sobre pdf.*",
    r"si necesitas informacion sobre pdf.*",
    r"si necesitas un documento.*"

]


# =====================================
# CLEAN RESPONSE
# =====================================

def sanitize_assistant_memory(
    response: str
) -> str:

    cleaned = response

    for pattern in CONTAMINATION_PATTERNS:

        cleaned = re.sub(
            pattern,
            "",
            cleaned,
            flags=re.IGNORECASE
        )

    cleaned = cleaned.strip()

    return cleaned
