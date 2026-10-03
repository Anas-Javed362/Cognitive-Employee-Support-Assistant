import os

models_code = {
    'employee.py': '''from sqlalchemy import Column, String, Integer
from app.db.database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String)
    department = Column(String)
    email = Column(String, unique=True, index=True)
    manager = Column(String)
    role = Column(String)
    hashed_password = Column(String)
''',
    'ticket.py': '''from sqlalchemy import Column, String, Integer, DateTime
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
''',
    'request.py': '''from sqlalchemy import Column, String, Integer, DateTime, Date
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
''',
    'escalation.py': '''from sqlalchemy import Column, String, Integer, DateTime, Text
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
''',
    'knowledge.py': '''from sqlalchemy import Column, String, Integer, DateTime, Text
from app.db.database import Base
from datetime import datetime

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, index=True)
    document_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)
    chunk_id = Column(String, unique=True, index=True)
    content = Column(Text)
    section = Column(String)
    page_number = Column(Integer, nullable=True)
'''
}

schemas_code = {
    'employee.py': '''from pydantic import BaseModel
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
''',
    'ticket.py': '''from pydantic import BaseModel
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
''',
    'request.py': '''from pydantic import BaseModel
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
''',
    'escalation.py': '''from pydantic import BaseModel
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
''',
    'chat.py': '''from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    intent: Optional[str] = None
    sources: Optional[List[str]] = []
    workflow_status: Optional[str] = None
'''
}

core_code = {
    'security.py': '''from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
''',
    'logging.py': '''import logging
import sys

def setup_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

logger = setup_logging()
'''
}

for fname, content in models_code.items():
    with open(f'backend/app/models/{fname}', 'w') as f:
        f.write(content)

for fname, content in schemas_code.items():
    with open(f'backend/app/schemas/{fname}', 'w') as f:
        f.write(content)

for fname, content in core_code.items():
    with open(f'backend/app/core/{fname}', 'w') as f:
        f.write(content)
