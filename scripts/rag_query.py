import chromadb
from sentence_transformers import SentenceTransformer
import ollama
import os

DB_DIR = os.path.expanduser("~/jarvis/rag/db")

client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_collection("jarvis_docs")

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

while True:

    query = input("\nConsulta: ")

    if query.lower() in ["exit", "quit"]:
        break

    print("\nGenerando embedding...")

    query_embedding = embed_model.encode(query).tolist()

    print("Buscando contexto relevante...")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context_chunks = results["documents"][0]

    context = "\n\n".join(context_chunks)

    prompt = f"""
Eres Jarvis, un asistente documental jurídico y técnico.

Debes responder EXCLUSIVAMENTE usando el contexto proporcionado.

Si la respuesta no aparece claramente en el contexto, di:
"No encuentro esa información en los documentos."

CONTEXTO:
{context}

PREGUNTA:
{query}

RESPUESTA:
"""

    print("\nConsultando LLM...\n")

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    print("\n" + "="*80)
    print("RESPUESTA:\n")
    print(answer)
    print("\n" + "="*80)
