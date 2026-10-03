from langchain_community.vectorstores import FAISS
from app.rag.embeddings import EmbeddingService
from langchain.schema import Document
import os
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, store_path="./data/vector_store"):
        self.store_path = store_path
        self.embedding_service = EmbeddingService().get_embeddings()
        self.store = None
        
        if os.path.exists(self.store_path):
            try:
                self.store = FAISS.load_local(self.store_path, self.embedding_service, allow_dangerous_deserialization=True)
                logger.info("Loaded existing FAISS vector store")
            except Exception as e:
                logger.error(f"Failed to load vector store: {e}")
                
    def add_documents(self, documents):
        if not self.embedding_service:
            logger.error("Embedding service not available")
            return
            
        if self.store is None:
            self.store = FAISS.from_documents(documents, self.embedding_service)
        else:
            self.store.add_documents(documents)
            
        # Save local
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        self.store.save_local(self.store_path)
        logger.info(f"Saved vector store to {self.store_path}")
        
    def similarity_search(self, query: str, top_k: int = 3):
        if not self.store:
            logger.warning("No vector store loaded for search")
            return []
        return self.store.similarity_search(query, k=top_k)
