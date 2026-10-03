from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.knowledge import KnowledgeDocument
from typing import List

router = APIRouter()

@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(KnowledgeDocument).all()
    return [{"id": d.id, "name": d.document_name, "type": d.document_type} for d in docs]
