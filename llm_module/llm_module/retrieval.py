"""Retrieval layer that composes embedding generation and vector store.

This module clearly separates:
- embedding generation (`embeddings`)
- vector storage (`InMemoryVectorStore`)
- similarity computation (in the store)
- query handling (`Retriever` API)

It also includes a simple keyword matcher for comparison experiments.
"""
from typing import List, Dict, Any
import os
from .embeddings import batch_embed, text_to_embedding
from .vector_store import InMemoryVectorStore

# Try to import FAISS-backed store if available
_HAS_FAISS = False
_FAISS_ENABLED = os.getenv("USE_FAISS", "0") in ("1", "true", "True")
if _FAISS_ENABLED:
    try:
        from .faiss_vector_store import FaissVectorStore
        _HAS_FAISS = True
    except Exception:
        _HAS_FAISS = False


class Retriever:
    def __init__(self, use_faiss: bool = False):
        """Create a Retriever.

        If `use_faiss=True` and FAISS is available, a FAISS-backed store will be
        used. Otherwise falls back to the in-memory store.
        """
        self.use_faiss = use_faiss and _HAS_FAISS
        self.store = InMemoryVectorStore() if not self.use_faiss else None

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        metadatas = metadatas or [{} for _ in texts]
        ids = ids or [str(i) for i in range(len(texts))]
        embs = batch_embed(texts)
        docs = []
        for i, t in enumerate(texts):
            docs.append({
                'id': ids[i],
                'text': t,
                'metadata': metadatas[i],
                'embedding': embs[i]
            })
        # Initialize FAISS store on first add if requested
        if self.use_faiss:
            if self.store is None:
                dim = len(embs[0]) if len(embs) else 0
                self.store = FaissVectorStore(dim)
            self.store.add_documents(docs)
        else:
            self.store.add_documents(docs)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        q_emb = text_to_embedding(query)
        scored = self.store.similarity_search(q_emb, top_k=top_k)
        return [{'id': r['id'], 'text': r['text'], 'metadata': r.get('metadata', {}), 'score': s} for r, s in scored]

    def keyword_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        # simple substring match count ranking
        q = query.lower()
        scored = []
        for r in self.store.records:
            count = r['text'].lower().count(q)
            scored.append((r, count))
        scored.sort(key=lambda x: x[1], reverse=True)
        # convert count to pseudo-score in [0,1]
        results = []
        for r, cnt in scored[:top_k]:
            score = float(cnt)
            results.append({'id': r['id'], 'text': r['text'], 'metadata': r.get('metadata', {}), 'score': score})
        return results
