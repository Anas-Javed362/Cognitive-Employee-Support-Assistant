from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    category: str
    issue: str
    priority: str

class Ticket(BaseModel):
    ticket_id: str
    employee_id: str
    category: str
    issue: str
    priority: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True
