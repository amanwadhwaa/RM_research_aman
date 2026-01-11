from embeddings.embedder import Embedder
from embeddings.store import VectorStore
from retrieval.semantic_search import SemanticSearch
from rag.pipeline import RAGPipeline

from llm.controlled_llm import ControlledLLM  

embedder = Embedder()
dim = len(embedder.embed("test"))

store = VectorStore(dim)


docs = open("data/documents.txt").read().split("\n")

for i, doc in enumerate(docs):
    if doc.strip():
        emb = embedder.embed(doc)
        store.add(emb, doc, source="docs", doc_id=i)

retriever = SemanticSearch(store)
llm = ControlledLLM()
rag = RAGPipeline(embedder, retriever, llm)

# 1️⃣ semantic > keyword
print(rag.answer("How do plants use sunlight?"))

# 2️⃣ grounded failure
print(rag.answer("Explain black holes"))  # should fail or say "I don't know"
