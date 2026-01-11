class RAGPipeline:
    def __init__(self, embedder, retriever, llm):
        self.embedder = embedder
        self.retriever = retriever
        self.llm = llm  
    def answer(self, query: str):
        query_embedding = self.embedder.embed(query)
        results = self.retriever.search(query_embedding)

        if not results:
            raise RuntimeError("No relevant context retrieved")

        context = "\n\n".join(
            [item["text"] for item in results]
        )

        prompt = f"""
You are a grounded assistant.
Answer the question using ONLY the context below.
If the answer is not present, say you don't know.

Context:
{context}

Question:
{query}
"""

        return self.llm.generate(prompt)
