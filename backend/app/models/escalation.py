from sqlalchemy import Column, String, Integer, DateTime, Text
from app.db.database import Base
from datetime import datetime

class Escalation(Base):
    __tablename__ = "escalations"
    id = Column(Integer, primary_key=True, index=True)
    escalation_id = Column(String, unique=True, index=True)
    employee_id = Column(String, index=True)
    reason = Column(String)
    conversation_context = Column(Text)
    requested_action = Column(String)
    priority = Column(String)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)
