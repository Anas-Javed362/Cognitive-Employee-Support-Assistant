import os

api_code = {
    'chat.py': '''from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.intent_router import IntentRouter
from app.services.workflow_engine import WorkflowEngine
from app.rag.retrieval import RAGService
from app.ai.providers.local import LocalLLMProvider

router = APIRouter()
intent_router = IntentRouter()
workflow_engine = WorkflowEngine()
rag_service = RAGService()
llm_provider = LocalLLMProvider()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    intent = intent_router.route(request.message)
    
    if intent == "KNOWLEDGE_QUERY":
        rag_result = rag_service.query(request.message)
        context = rag_result.get("context", "")
        sources = rag_result.get("sources", [])
        
        prompt = f"Answer the user based on the context.\\nContext: {context}\\nQuestion: {request.message}"
        response_text = llm_provider.generate(prompt)
        
        if not context.strip():
            response_text = "I couldn't find enough information in the approved company knowledge base to answer that confidently. Would you like me to escalate this?"
            
        return ChatResponse(
            response=response_text,
            intent=intent,
            sources=sources,
            workflow_status="COMPLETED"
        )
        
    workflow_result = workflow_engine.execute(intent, {"message": request.message})
    
    return ChatResponse(
        response=workflow_result.get("message"),
        intent=intent,
        workflow_status=workflow_result.get("workflow_status")
    )
''',
    'tickets.py': '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, Ticket as TicketSchema
import uuid
from typing import List

router = APIRouter()

@router.post("/", response_model=TicketSchema)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = Ticket(
        ticket_id=f"INC-{str(uuid.uuid4())[:8].upper()}",
        employee_id="EMP1024", # Mock auth
        category=ticket.category,
        issue=ticket.issue,
        priority=ticket.priority
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.get("/{ticket_id}", response_model=TicketSchema)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/", response_model=List[TicketSchema])
def list_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).all()
''',
    'requests.py': '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.request import EmployeeRequest
from app.schemas.request import EmployeeRequestCreate, EmployeeRequest as RequestSchema
import uuid
from typing import List

router = APIRouter()

@router.post("/", response_model=RequestSchema)
def create_request(req: EmployeeRequestCreate, db: Session = Depends(get_db)):
    db_req = EmployeeRequest(
        request_id=f"REQ-{str(uuid.uuid4())[:8].upper()}",
        employee_id="EMP1024",
        request_type=req.request_type,
        date=req.date,
        reason=req.reason
    )
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

@router.get("/{request_id}", response_model=RequestSchema)
def get_request(request_id: str, db: Session = Depends(get_db)):
    req = db.query(EmployeeRequest).filter(EmployeeRequest.request_id == request_id).first()
    if req is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return req

@router.get("/", response_model=List[RequestSchema])
def list_requests(db: Session = Depends(get_db)):
    return db.query(EmployeeRequest).all()
''',
    'escalations.py': '''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.escalation import Escalation
from app.schemas.escalation import EscalationCreate, Escalation as EscalationSchema
import uuid
from typing import List

router = APIRouter()

@router.post("/", response_model=EscalationSchema)
def create_escalation(esc: EscalationCreate, db: Session = Depends(get_db)):
    db_esc = Escalation(
        escalation_id=f"ESC-{str(uuid.uuid4())[:8].upper()}",
        employee_id="EMP1024",
        reason=esc.reason,
        conversation_context=esc.conversation_context,
        requested_action=esc.requested_action,
        priority=esc.priority
    )
    db.add(db_esc)
    db.commit()
    db.refresh(db_esc)
    return db_esc

@router.get("/", response_model=List[EscalationSchema])
def list_escalations(db: Session = Depends(get_db)):
    return db.query(Escalation).all()
''',
    'knowledge.py': '''from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.knowledge import KnowledgeDocument
from typing import List

router = APIRouter()

@router.get("/")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(KnowledgeDocument).all()
    return [{"id": d.id, "name": d.document_name, "type": d.document_type} for d in docs]
'''
}

main_code = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, tickets, requests, escalations, knowledge
from app.db.database import engine, Base
import app.models.employee
import app.models.ticket
import app.models.request
import app.models.escalation
import app.models.knowledge

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cognitive Employee Support Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(tickets.router, prefix="/api/tickets", tags=["tickets"])
app.include_router(requests.router, prefix="/api/employee-requests", tags=["requests"])
app.include_router(escalations.router, prefix="/api/escalations", tags=["escalations"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/metrics/summary")
def metrics():
    return {"status": "ok", "total_requests": 100}
'''

for fname, content in api_code.items():
    with open(f'backend/app/api/routes/{fname}', 'w') as f:
        f.write(content)

with open('backend/app/main.py', 'w') as f:
    f.write(main_code)
