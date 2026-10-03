from langchain_community.embeddings import HuggingFaceEmbeddings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        except Exception as e:
            logger.error(f"Failed to load local embeddings: {e}")
            self.embeddings = None
    
    def get_embeddings(self):
        return self.embeddings
