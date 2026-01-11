class SemanticSearch:
    def __init__(self, vector_store):
        self.store = vector_store

    def search(self, query_embedding, top_k=3):
        return self.store.search(query_embedding, top_k)
