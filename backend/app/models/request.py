from sqlalchemy import Column, String, Integer, DateTime, Date
from app.db.database import Base
from datetime import datetime

class EmployeeRequest(Base):
    __tablename__ = "employee_requests"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True)
    employee_id = Column(String, index=True)
    request_type = Column(String)
    date = Column(String)
    reason = Column(String)
    status = Column(String, default="PENDING_APPROVAL")
    approver = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
