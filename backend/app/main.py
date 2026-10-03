from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.api.routes import chat, tickets, requests, escalations, knowledge
from app.db.database import engine, Base, get_db
from app.models.ticket import Ticket
from app.models.request import EmployeeRequest
from app.models.escalation import Escalation
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
def metrics(db: Session = Depends(get_db)):
    open_tickets = db.query(Ticket).filter(Ticket.status == "OPEN").count()
    total_tickets = db.query(Ticket).count()
    pending_requests = db.query(EmployeeRequest).filter(EmployeeRequest.status == "PENDING_APPROVAL").count()
    total_requests = db.query(EmployeeRequest).count()
    open_escalations = db.query(Escalation).filter(Escalation.status == "OPEN").count()
    return {
        "status": "ok",
        "open_tickets": open_tickets,
        "total_tickets": total_tickets,
        "pending_requests": pending_requests,
        "total_requests": total_requests,
        "open_escalations": open_escalations,
    }

