import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)  
        self.texts = []
        self.meta = []

    def add(self, embedding, text, source, doc_id):
        vec = np.array([embedding]).astype("float32")
        self.index.add(vec)

        self.texts.append(text)
        self.meta.append({
            "source": source,
            "id": doc_id
        })

    def search(self, query_embedding, top_k=3):
        q = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(q, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            results.append({
                "score": float(score),
                "text": self.texts[idx],
                "meta": self.meta[idx]
            })

        return results
