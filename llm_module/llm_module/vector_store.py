"""In-memory vector store for embeddings + metadata.

Stores records as simple dicts and supports top-k cosine similarity search.
This keeps storage and similarity computation clearly separated.
"""
from typing import List, Dict, Any, Tuple
import math


def _cosine(a: List[float], b: List[float]) -> float:
    # assume vectors are normalized; if not, handle gracefully
    dot = sum(x * y for x, y in zip(a, b))
    norma = math.sqrt(sum(x * x for x in a)) or 1.0
    normb = math.sqrt(sum(x * x for x in b)) or 1.0
    return dot / (norma * normb)


class InMemoryVectorStore:
    def __init__(self):
        # records: list of dicts {id, text, metadata, embedding}
        self.records: List[Dict[str, Any]] = []

    def add_documents(self, docs: List[Dict[str, Any]]):
        """Add multiple documents. Each doc should include keys:
        - 'id' (str), 'text' (str), 'metadata' (dict), 'embedding' (List[float])
        """
        for d in docs:
            assert 'id' in d and 'text' in d and 'embedding' in d
            self.records.append(d)

    def similarity_search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Return top_k records sorted by cosine similarity.

        Returns list of tuples (record, score) with score in [-1,1].
        """
        scored = []
        for r in self.records:
            score = _cosine(query_embedding, r['embedding'])
            scored.append((r, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
