from fastapi import APIRouter, Depends, HTTPException
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
