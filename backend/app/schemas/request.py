from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmployeeRequestCreate(BaseModel):
    request_type: str
    date: str
    reason: str

class EmployeeRequest(BaseModel):
    request_id: str
    employee_id: str
    request_type: str
    date: str
    reason: str
    status: str
    approver: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True
