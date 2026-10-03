import os

ai_code = {
    'base.py': '''from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        pass
''',
    'watsonx.py': '''from app.ai.providers.base import BaseLLMProvider
from app.core.config import settings
from app.core.logging import logger

class WatsonxProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.WATSONX_API_KEY
        self.project_id = settings.WATSONX_PROJECT_ID
        self.url = settings.WATSONX_URL
        self.model_id = settings.WATSONX_MODEL_ID
        
        if not all([self.api_key, self.project_id, self.url, self.model_id]):
            logger.warning("Watsonx credentials incomplete. Falling back to local/mock behavior.")
            self.is_ready = False
        else:
            self.is_ready = True
            
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        if not self.is_ready:
            return "Mock response from WatsonxProvider. Please configure Watsonx credentials."
        # In a real scenario we'd use ibm_watson_machine_learning here
        return f"[Watsonx] Response to: {prompt[:50]}..."
''',
    'local.py': '''from app.ai.providers.base import BaseLLMProvider

class LocalLLMProvider(BaseLLMProvider):
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        if "wfh" in prompt.lower() or "work from home" in prompt.lower():
            return "According to the policy, employees may work from home pending manager approval."
        if "laptop" in prompt.lower() or "wi-fi" in prompt.lower():
            return "Please create an IT ticket for hardware and network issues."
        if "password" in prompt.lower():
            return "You can reset your password using the self-service portal."
        if "delete my employee account" in prompt.lower():
            return "This requires human approval. Escalating."
        return f"Local fallback response to: {prompt[:50]}..."
'''
}

rag_code = {
    'embeddings.py': '''from langchain_community.embeddings import HuggingFaceEmbeddings
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
''',
    'vector_store.py': '''from langchain_community.vectorstores import FAISS
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
''',
    'retrieval.py': '''from app.rag.vector_store import VectorStore

class RAGService:
    def __init__(self):
        self.vector_store = VectorStore()
        
    def query(self, question: str):
        docs = self.vector_store.similarity_search(question)
        sources = []
        context = ""
        for d in docs:
            context += d.page_content + "\\n"
            source_name = d.metadata.get("source", "Unknown Document")
            if source_name not in sources:
                sources.append(source_name)
                
        return {
            "context": context,
            "sources": sources
        }
'''
}

services_code = {
    'intent_router.py': '''from app.ai.providers.local import LocalLLMProvider

class IntentRouter:
    def __init__(self):
        self.llm = LocalLLMProvider()
        
    def route(self, message: str) -> str:
        msg_lower = message.lower()
        if "policy" in msg_lower or "password" in msg_lower or "reimbursement" in msg_lower:
            return "KNOWLEDGE_QUERY"
        elif "laptop" in msg_lower or "wi-fi" in msg_lower or "vpn" in msg_lower or "ticket" in msg_lower or "support" in msg_lower:
            return "IT_SUPPORT"
        elif "work from home" in msg_lower or "wfh" in msg_lower or "leave" in msg_lower:
            return "WFH_REQUEST"
        elif "delete" in msg_lower and "account" in msg_lower:
            return "HUMAN_ESCALATION"
        elif "status" in msg_lower and "ticket" in msg_lower:
            return "TICKET_STATUS"
        elif "status" in msg_lower and "request" in msg_lower:
            return "REQUEST_STATUS"
        return "UNKNOWN"
''',
    'workflow_engine.py': '''class WorkflowEngine:
    def __init__(self, db_session=None):
        self.db = db_session
        
    def execute(self, intent: str, context: dict):
        if intent == "IT_SUPPORT":
            return {"status": "SUCCESS", "message": "Ticket created.", "workflow_status": "COMPLETED"}
        elif intent == "WFH_REQUEST":
            return {"status": "SUCCESS", "message": "WFH Request submitted pending approval.", "workflow_status": "PENDING_APPROVAL"}
        elif intent == "HUMAN_ESCALATION":
            return {"status": "ESCALATED", "message": "Request requires human approval. Escalating.", "workflow_status": "ESCALATED"}
        elif intent == "KNOWLEDGE_QUERY":
            return {"status": "SUCCESS", "message": "Knowledge retrieved.", "workflow_status": "COMPLETED"}
        
        return {"status": "FAILED", "message": "Unknown workflow.", "workflow_status": "FAILED"}
'''
}

for fname, content in ai_code.items():
    with open(f'backend/app/ai/providers/{fname}', 'w') as f:
        f.write(content)

for fname, content in rag_code.items():
    with open(f'backend/app/rag/{fname}', 'w') as f:
        f.write(content)

for fname, content in services_code.items():
    with open(f'backend/app/services/{fname}', 'w') as f:
        f.write(content)
