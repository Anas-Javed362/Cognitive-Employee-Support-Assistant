from app.rag.vector_store import VectorStore

class RAGService:
    def __init__(self):
        self.vector_store = VectorStore()
        
    def query(self, question: str):
        docs = self.vector_store.similarity_search(question)
        sources = []
        context = ""
        for d in docs:
            context += d.page_content + "\n"
            source_name = d.metadata.get("source", "Unknown Document")
            if source_name not in sources:
                sources.append(source_name)
                
        return {
            "context": context,
            "sources": sources
        }
