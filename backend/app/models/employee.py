from sqlalchemy import Column, String, Integer
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
