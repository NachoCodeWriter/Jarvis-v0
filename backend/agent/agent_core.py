from datetime import datetime

from backend.agent.orchestrator import ask_llm
from backend.agent.router import detect_intent
from backend.agent.tool_executor import execute_tool

from backend.context.context_manager import (
    build_context
)

from backend.memory.memory_sanitizer import (
    sanitize_assistant_memory
)

from backend.memory.session_memory import (
    add_message
)

from backend.memory.memory_dispatcher import (
    dispatch_memory_event
)

from backend.memory.cognitive_pipeline import (
    process_cognitive_memory
)

from backend.utils.logger import (
    system_logger,
    tool_logger,
    memory_logger,
    error_logger
)

# =========================================
# CHAT RESPONSE PIPELINE
# =========================================

def generate_chat_response(
    prompt: str
) -> dict:

    try:

        # ---------------------------------
        # BUILD CONTEXT
        # ---------------------------------

        final_prompt = build_context(
            prompt
        )

        # ---------------------------------
        # LLM CALL
        # ---------------------------------

        response = ask_llm(
            final_prompt
        )

        # ------------------------------
        # SAVE ASSISTANT MESSAGE
        # ------------------------------

        sanitized_response = sanitize_assistant_memory(
            response
        )

        if sanitized_response:

            message_id = add_message(
                role="assistant",
                content=sanitized_response
            )

            if (
                message_id is not None
                and sanitized_response
            ):

                dispatch_memory_event(
                    memory_id=message_id,
                    role="assistant",
                    content=sanitized_response,
                    timestamp=(
                        datetime.utcnow().isoformat()
                    )
                )

        # ---------------------------------
        # COMPACT LOGGING
        # ---------------------------------

        memory_logger.info(
            f"""
CHAT RESPONSE GENERATED

Prompt:
{prompt}

Response Length:
{len(response)}
"""
        )

        return {
            "tool": "chat",
            "response": response
        }

    except Exception as error:

        error_logger.error(
            f"Error generando chat response: {error}"
        )

        return {
            "tool": "chat",
            "response": "Ha ocurrido un error procesando la respuesta."
        }

# =========================================
# TOOL EXECUTION PIPELINE
# =========================================

def process_tool(
    intent: str,
    prompt: str
):

    try:

        tool_result = execute_tool(
            intent,
            prompt
        )

        if tool_result is None:
            return None

        # ---------------------------------
        # COMPACT TOOL LOGGING
        # ---------------------------------

        tool_logger.info(
            f"""
TOOL EXECUTED

Intent:
{intent}

Prompt:
{prompt}
"""
        )

        return tool_result

    except Exception as error:

        error_logger.error(
            f"Error ejecutando tool: {error}"
        )

        return None

# =========================================
# MAIN AGENT PIPELINE
# =========================================

def process_prompt(
    prompt: str
):

    try:

        # ---------------------------------
        # SAVE USER MESSAGE
        # ---------------------------------

        timestamp = (
            datetime.utcnow().isoformat()
        )

        message_id = add_message(
            role="user",
            content=prompt
        )

        if message_id is not None:
            dispatch_memory_event(
                memory_id=message_id,
                role="user",
                content=prompt,
                timestamp=timestamp
            )

            cognitive_result = (
                process_cognitive_memory(
                    role="user",
                    content=prompt
            )
        )

            memory_logger.info(
                f"""
PASSIVE COGNITIVE ANALYSIS

Classification:
{cognitive_result.get("classification")}
"""
            )


        # ---------------------------------
        # DETECT INTENT
        # ---------------------------------

        intent = detect_intent(
            prompt
        )

        system_logger.info(
            f"Intent detectado: {intent}"
        )

        # ---------------------------------
        # TOOL EXECUTION
        # ---------------------------------

        if intent != "chat":

            tool_response = process_tool(
                intent,
                prompt
            )

            if tool_response is not None:
                return tool_response

        # ---------------------------------
        # CHAT FALLBACK
        # ---------------------------------

        return generate_chat_response(
            prompt
        )

    except Exception as error:

        error_logger.error(
            f"Error en process_prompt: {error}"
        )

        return {
            "tool": "error",
            "response": "Ha ocurrido un error interno."
        }
