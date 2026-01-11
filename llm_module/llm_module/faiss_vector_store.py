"""FAISS-backed vector store adapter.

This module provides a thin adapter around FAISS for efficient
similarity search. If FAISS is not installed, importing this module
will raise ImportError; callers should handle that gracefully and
fall back to the in-memory store.
"""
from typing import List, Dict, Any, Tuple
import numpy as np

try:
    import faiss
except Exception as e:
    raise ImportError("faiss is not available") from e


class FaissVectorStore:
    def __init__(self, dim: int):
        # Use inner-product on normalized vectors to simulate cosine
        self.dim = dim
        self.index = faiss.IndexIDMap(faiss.IndexFlatIP(dim))
        # map internal int ids -> record dict
        self.id_to_record: Dict[int, Dict[str, Any]] = {}
        self._next_id = 1

    def add_documents(self, docs: List[Dict[str, Any]]):
        vecs = []
        ids = []
        for d in docs:
            assert 'embedding' in d
            emb = np.array(d['embedding'], dtype='float32')
            # normalize
            norm = np.linalg.norm(emb) or 1.0
            emb = emb / norm
            vecs.append(emb)
            idx = self._next_id
            ids.append(idx)
            self.id_to_record[idx] = d
            self._next_id += 1
        if len(vecs) == 0:
            return
        matrix = np.stack(vecs).astype('float32')
        ids_arr = np.array(ids, dtype='int64')
        self.index.add_with_ids(matrix, ids_arr)

    def similarity_search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        q = np.array(query_embedding, dtype='float32')
        norm = np.linalg.norm(q) or 1.0
        q = (q / norm).astype('float32')
        q = q.reshape(1, -1)
        D, I = self.index.search(q, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            rec = self.id_to_record.get(int(idx))
            results.append((rec, float(score)))
        return results
