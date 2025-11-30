import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Global FAISS index
embedding_dim = 384
index = faiss.IndexFlatL2(embedding_dim)

resume_metadata = []   # Stores names + file names

def embed_text(text: str):
    """Return embedding or None safely."""
    try:
        vector = model.encode([text])[0]
        return np.array(vector).astype("float32")
    except Exception as e:
        print("Embedding error:", e)
        return None


def add_resume_to_faiss(name: str, text: str, filename: str):
    """Add resume embedding to FAISS index."""
    emb = embed_text(text)
    if emb is None:
        raise ValueError("Embedding returned None")

    global index, resume_metadata

    emb = np.expand_dims(emb, axis=0)
    index.add(emb)

    resume_metadata.append({
        "name": name,
        "filename": filename
    })


def query_similar_resumes(query_text: str, top_k: int = 3):
    if len(resume_metadata) == 0:
        return []

    emb = embed_text(query_text)
    if emb is None:
        return []

    emb = np.expand_dims(emb, axis=0)

    distances, indices = index.search(emb, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(resume_metadata):
            results.append(resume_metadata[idx])

    return results
