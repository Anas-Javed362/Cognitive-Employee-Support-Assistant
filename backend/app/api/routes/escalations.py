from fastapi import APIRouter, Depends, HTTPException
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
