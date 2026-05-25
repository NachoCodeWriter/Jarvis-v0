# =========================================
# INTENT KEYWORDS
# =========================================

INTENT_KEYWORDS = {

    "file_read": [
        "lee archivo",
        "abre archivo",
        "leer archivo",
        "mostrar archivo",
        "contenido del archivo"
    ],

    "file_search": [
        "busca archivo",
        "localiza archivo",
        "encuentra archivo",
        "buscar pdf",
        "buscar documento"
    ],


    "rag": [
        "contrato",
        "documento",
        "cláusula",
        "penalización",
        "penalizaciones",
        "obra",
        "sentencia",
        "pdf",
        "escrito",
        "expediente"
    ]
}


# =========================================
# INTENT DETECTION
# =========================================

def detect_intent(prompt: str):

    text = prompt.lower().strip()

    for intent, keywords in INTENT_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:
                return intent

    return "chat"
