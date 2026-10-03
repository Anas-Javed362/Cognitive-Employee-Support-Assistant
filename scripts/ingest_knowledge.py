import os
import glob
from langchain.schema import Document
from app.rag.vector_store import VectorStore
from app.db.database import SessionLocal, engine, Base
from app.models.knowledge import KnowledgeDocument, KnowledgeChunk
import uuid

def ingest_knowledge():
    Base.metadata.create_all(bind=engine)
    vector_store = VectorStore()
    db = SessionLocal()
    
    docs = []
    knowledge_dir = "knowledge"
    for filepath in glob.glob(f"{knowledge_dir}/*.md"):
        filename = os.path.basename(filepath)
        with open(filepath, "r") as f:
            content = f.read()
            
        doc = Document(
            page_content=content,
            metadata={"source": filename}
        )
        docs.append(doc)
        
        # Save to DB
        if not db.query(KnowledgeDocument).filter(KnowledgeDocument.document_name == filename).first():
            db_doc = KnowledgeDocument(document_name=filename, document_type="markdown")
            db.add(db_doc)
            db.commit()
            db.refresh(db_doc)
            
            db_chunk = KnowledgeChunk(
                document_id=db_doc.id,
                chunk_id=str(uuid.uuid4()),
                content=content,
                section="full"
            )
            db.add(db_chunk)
            db.commit()
            
    if docs:
        vector_store.add_documents(docs)
        print("Knowledge ingestion complete.")
    else:
        print("No documents found in knowledge directory.")

if __name__ == "__main__":
    ingest_knowledge()
