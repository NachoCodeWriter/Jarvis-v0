import ollama

from backend.config.settings import (
    MODEL_NAME,
    SYSTEM_PROMPT,
    TEMPERATURE
)

from backend.utils.logger import (
    llm_logger,
    error_logger
)


# =========================================
# MESSAGE BUILDER
# =========================================

def build_messages(prompt: str):

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ]


# =========================================
# RESPONSE EXTRACTION
# =========================================

def extract_response(response):

    return response["message"]["content"]


# =========================================
# MAIN LLM CALL
# =========================================

def ask_llm(prompt: str):

    messages = build_messages(prompt)

    llm_logger.info("Construyendo llamada al LLM")

    llm_logger.info(f"Prompt recibido: {prompt}")

    try:

        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            options={
                "temperature": TEMPERATURE
            }
        )

        final_response = extract_response(response)

        llm_logger.info("Respuesta generada correctamente")

        return final_response

    except Exception as error:

        error_logger.error(f"LLM ERROR: {str(error)}")

        print(f"\n[LLM ERROR] {error}")

        return "Ha ocurrido un error al consultar el modelo."
