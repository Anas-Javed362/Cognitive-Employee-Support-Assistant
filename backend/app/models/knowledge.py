from sqlalchemy import Column, String, Integer, DateTime, Text
from app.db.database import Base
from datetime import datetime

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, index=True)
    document_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)
    chunk_id = Column(String, unique=True, index=True)
    content = Column(Text)
    section = Column(String)
    page_number = Column(Integer, nullable=True)
