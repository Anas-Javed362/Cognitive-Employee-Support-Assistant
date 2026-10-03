from pydantic import BaseModel
from datetime import datetime

class EscalationCreate(BaseModel):
    reason: str
    conversation_context: str
    requested_action: str
    priority: str

class Escalation(BaseModel):
    escalation_id: str
    employee_id: str
    reason: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True
