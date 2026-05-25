import os
import chromadb
import fitz
from sentence_transformers import SentenceTransformer

INPUT_DIR = os.path.expanduser("~/jarvis/rag/input")
DB_DIR = os.path.expanduser("~/jarvis/rag/db")

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection("jarvis_docs")

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text

def chunk_text(text, chunk_size=1200, overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

for filename in os.listdir(INPUT_DIR):

    if filename.endswith(".pdf"):

        path = os.path.join(INPUT_DIR, filename)

        print(f"\nProcesando: {filename}")

        text = extract_text_from_pdf(path)

        chunks = chunk_text(text)

        print(f"Chunks generados: {len(chunks)}")

        for i, chunk in enumerate(chunks):

            embedding = embed_model.encode(chunk).tolist()

            collection.add(
                ids=[f"{filename}_{i}"],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "source": filename,
                    "chunk": i
                }]
            )

        print(f"Indexado completo: {filename}")

print("\nRAG ingestion completada")

