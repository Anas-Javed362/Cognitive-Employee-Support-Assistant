from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    department: str
    email: str
    manager: Optional[str] = None
    role: str

class EmployeeCreate(EmployeeBase):
    password: str

class Employee(EmployeeBase):
    id: int
    class Config:
        from_attributes = True
