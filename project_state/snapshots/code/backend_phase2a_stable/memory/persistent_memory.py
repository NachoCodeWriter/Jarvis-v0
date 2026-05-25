import sqlite3
from datetime import datetime

from backend.config.settings import (
    MEMORY_DB_PATH,
    MEMORY_LIMIT
)

from backend.utils.logger import (
    memory_logger,
    error_logger
)

# ============================================
# DATABASE CONNECTION
# ============================================

def get_connection():

    return sqlite3.connect(MEMORY_DB_PATH)


# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_db():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            conn.commit()

        memory_logger.info("Base de datos de memoria inicializada")

    except Exception as error:

        error_logger.error(f"Error inicializando memoria: {error}")


# ============================================
# ADD MESSAGE
# ============================================

def add_message(
    role: str,
    content: str,
) -> int | None:

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO messages (
                    role,
                    content,
                    created_at
                )
                VALUES (?, ?, ?)
                """,
                (
                    role,
                    content,
                    datetime.utcnow().isoformat()
                )
            )

            conn.commit()

            message_id = cursor.lastrowid

            memory_logger.info(
            f"Mensaje guardado: {role} | ID: {message_id}"
            )

            return message_id

    except Exception as error:

        error_logger.error(
            f"Error guardando mensaje: {error}"
        )

        return None


# ============================================
# GET RECENT MESSAGES
# ============================================

def get_recent_messages(limit: int = MEMORY_LIMIT):

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT role, content
                FROM messages
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            )

            rows = cursor.fetchall()

        rows.reverse()

        memory_logger.info(
            f"Recuperados {len(rows)} mensajes"
        )

        return [
            {
                "role": row[0],
                "content": row[1]
            }
            for row in rows
        ]

    except Exception as error:

        error_logger.error(
            f"Error recuperando memoria: {error}"
        )

        return []


# ============================================
# MEMORY CLEANUP
# ============================================

def clear_memory():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM messages"
            )

            conn.commit()

        memory_logger.warning(
            "Memoria eliminada"
        )

    except Exception as error:

        error_logger.error(
            f"Error limpiando memoria: {error}"
        )


# ============================================
# DATABASE BOOTSTRAP
# ============================================

init_db()
