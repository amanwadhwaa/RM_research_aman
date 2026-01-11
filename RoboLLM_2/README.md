# Task 3 – Knowledge-Grounded LLM System (RAG)

## Overview
This project implements a **knowledge-grounded Retrieval-Augmented Generation (RAG)** system.
Instead of answering purely from model memory, the LLM is grounded in external documents
retrieved using **semantic similarity**.

The controlled LLM module developed in **Task 2** is reused without modification.

---

## System Architecture
The system is explicitly divided into **two layers** to ensure clarity, debuggability,
and separation of concerns.

User Query
↓
Semantic Retrieval (Embeddings + FAISS)
↓
Relevant Context
↓
Controlled LLM (Task 2)
↓
Grounded Answer


---

## Layer 1: Semantic Retrieval System
This layer is responsible **only for retrieval**.  
No text generation happens here.

### Components
- **Embedding Generation**
  - Text is embedded locally using a sentence-transformer model.
  - Embeddings are deterministic and represent semantic meaning.
- **Vector Storage**
  - Embeddings are stored in an in-memory FAISS index.
  - Metadata (text, source, ID) is stored alongside vectors.
- **Similarity Search**
  - FAISS performs cosine-similarity based top-k retrieval.
  - Results are ranked by semantic relevance.

This layer enables semantic matching where keyword search would fail.

---

## Layer 2: Retrieval-Augmented Generation (RAG)
This layer combines:
- retrieved context from Layer 1
- the **controlled LLM module from Task 2**

### Grounding Behavior
- Retrieved text is injected into the prompt.
- The LLM is explicitly instructed to answer **only using the provided context**.
- If relevant information is missing, the system responds with *“I don’t know”*.

The LLM **cannot generate an answer without retrieval**, enforcing grounding by design.

---

## Failure Awareness & Experiments
The system explicitly demonstrates:
- semantic retrieval outperforming keyword matching
- grounded answers based on retrieved content
- failure cases due to poor or irrelevant retrieval
- how retrieval quality directly affects generation quality

These behaviors are showcased in `experiments/demo_cases.py`.

---

## Design Decisions
- **Local embeddings** are used to avoid vendor lock-in and quota limits.
- **FAISS** is used for efficient and scalable similarity search.
- Retrieval and generation are strictly separated to improve debuggability.
- The LLM is treated as a black box with validated outputs (Task 2).

---

## Limitations
- Uses a small in-memory document set.
- No document chunking or reranking is implemented.
- Retrieval quality is limited by document coverage.

---

## Outcome
This project results in:
- a working semantic search engine
- a grounded RAG pipeline
- a reusable foundation for future agent-based systems

# RM_research_aman
