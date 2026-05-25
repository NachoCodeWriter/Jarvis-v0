import chromadb

from sentence_transformers import (
    SentenceTransformer
)

from backend.config.settings import (
    RAG_DIR,
    EMBEDDING_MODEL,
    SEMANTIC_MEMORY_COLLECTION,
    MAX_EMBED_TEXT_CHARS
)

from backend.utils.logger import (
    create_logger
)


# =========================================
# LOGGER
# =========================================

semantic_memory_logger = create_logger(
    "semantic_memory_logger",
    "semantic_memory.log"
)


# =========================================
# CONSTANTS
# =========================================

DEFAULT_MEMORY_TYPE = "episodic"

DEFAULT_SOURCE = "conversation"


# =========================================
# EMBEDDING MODEL
# =========================================

semantic_memory_logger.info(
    "Loading embedding model..."
)

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL,
    device="cpu"
)

semantic_memory_logger.info(
    "Embedding model loaded"
)


# =========================================
# CHROMA CLIENT
# =========================================

semantic_memory_logger.info(
    "Initializing Chroma client..."
)

client = chromadb.PersistentClient(
    path=str(RAG_DIR / "db")
)

semantic_memory_logger.info(
    "Chroma client initialized"
)


# =========================================
# MEMORY COLLECTION
# =========================================

semantic_memory_logger.info(
    "Loading semantic memory collection..."
)

memory_collection = client.get_or_create_collection(
    name=SEMANTIC_MEMORY_COLLECTION
)

semantic_memory_logger.info(
    "Semantic memory collection ready"
)


# =========================================
# TEXT HELPERS
# =========================================

def truncate_for_embedding(
    text: str
) -> str:

    text = text.strip()

    if len(text) <= MAX_EMBED_TEXT_CHARS:
        return text

    return text[:MAX_EMBED_TEXT_CHARS]


def prepare_memory_text(
    content: str
) -> str:

    cleaned = truncate_for_embedding(
        content
    )

    return f"passage: {cleaned}"


def prepare_query_text(
    query: str
) -> str:

    cleaned = truncate_for_embedding(
        query
    )

    return f"query: {cleaned}"


# =========================================
# EMBEDDING GENERATION
# =========================================

def generate_embedding(
    text: str
):

    semantic_memory_logger.info(
        "Generating embedding..."
    )

    embedding = embedding_model.encode(
        text
    )

    semantic_memory_logger.info(
        "Embedding generated"
    )

    return embedding.tolist()


# =========================================
# MEMORY INDEXING
# =========================================

def index_memory(
    memory_id: int,
    role: str,
    content: str,
    timestamp: str,
    memory_type: str = DEFAULT_MEMORY_TYPE,
    source: str = DEFAULT_SOURCE,
    importance: float = 0.5
) -> bool:

    try:

        semantic_memory_logger.info(
            f"Indexing memory {memory_id}"
        )

        prepared_text = prepare_memory_text(
            content
        )

        embedding = generate_embedding(
            prepared_text
        )

        metadata = {
            "memory_id": str(memory_id),
            "role": role,
            "timestamp": timestamp,
            "memory_type": memory_type,
            "source": source,
            "importance": importance
        }

        memory_collection.add(
            ids=[str(memory_id)],
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata]
        )

        semantic_memory_logger.info(
            f"Memory indexed: {memory_id}"
        )

        return True

    except Exception as error:

        semantic_memory_logger.error(
            f"Semantic indexing failed: {error}"
        )

        return False


# =========================================
# SEMANTIC RETRIEVAL
# =========================================

def retrieve_semantic_memories(
    query: str,
    top_k: int
):

    try:

        semantic_memory_logger.info(
            "Starting semantic retrieval..."
        )

        prepared_query = prepare_query_text(
            query
        )

        query_embedding = generate_embedding(
            prepared_query
        )

        results = memory_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        semantic_memories = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            semantic_memories.append({
                "content": document,
                "score": distance,
                "metadata": metadata
            })

        semantic_memory_logger.info(
            f"Retrieved {len(semantic_memories)} semantic memories"
        )

        return semantic_memories

    except Exception as error:

        semantic_memory_logger.error(
            f"Semantic retrieval failed: {error}"
        )

        return []
