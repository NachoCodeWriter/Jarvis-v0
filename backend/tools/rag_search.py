import chromadb
from sentence_transformers import SentenceTransformer
import os


DB_DIR = os.path.expanduser("~/jarvis/rag/db")

client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_collection("jarvis_docs")

embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def rag_search(query, n_results=3):

    query_embedding = embed_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    documents = results["documents"][0]

    return documents
