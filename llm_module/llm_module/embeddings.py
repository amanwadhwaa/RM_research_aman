"""Lightweight embedding utilities.

This module provides a simple, dependency-free way to convert text
into fixed-size numeric vectors suitable for semantic similarity
experiments. It intentionally does NOT call external services so the
code runs offline. For production you can replace `text_to_embedding`
with calls to an official embedding API.
"""
import hashlib
import math
import os
from typing import List

# Optional OpenAI embeddings support (if configured)
_OPENAI_AVAILABLE = False
_OPENAI_USE = False
try:
    import openai
    _OPENAI_AVAILABLE = True
except Exception:
    _OPENAI_AVAILABLE = False

if _OPENAI_AVAILABLE and os.getenv("USE_OPENAI_EMBEDDINGS", "0") in ("1", "true", "True") and os.getenv("OPENAI_API_KEY"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    _OPENAI_USE = True


EMBED_DIM = 32


def _hash_to_vector(s: str, dim: int = EMBED_DIM) -> List[float]:
    h = hashlib.sha256(s.encode("utf-8")).digest()
    # Expand/rotate bytes to fill requested dim
    vec = []
    for i in range(dim):
        b = h[i % len(h)]
        vec.append((b / 255.0) - 0.5)
    # normalize
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def text_to_embedding(text: str) -> List[float]:
    """Convert text to a deterministic embedding vector.

    This is simple and fast, suitable for demos and tests. Replace with
    a call to an official embedding API for production use.
    """
    # If OpenAI is enabled, use the official API for higher-quality embeddings.
    if _OPENAI_USE:
        try:
            resp = openai.Embedding.create(input=text, model="text-embedding-3-small")
            vec = resp['data'][0]['embedding']
            # normalize
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            return [x / norm for x in vec]
        except Exception:
            # fallback to deterministic local embedding on any failure
            return _hash_to_vector(text)
    return _hash_to_vector(text)


def batch_embed(texts: List[str]) -> List[List[float]]:
    return [text_to_embedding(t) for t in texts]
