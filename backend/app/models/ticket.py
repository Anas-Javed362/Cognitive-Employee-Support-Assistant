from sqlalchemy import Column, String, Integer, DateTime
from app.db.database import Base
from datetime import datetime

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    employee_id = Column(String, index=True)
    category = Column(String)
    issue = Column(String)
    priority = Column(String)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    assigned_team = Column(String)
