import os
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.models.employee import Employee
from app.models.ticket import Ticket
from app.models.request import EmployeeRequest
from app.models.escalation import Escalation
from app.models.knowledge import KnowledgeDocument, KnowledgeChunk
import sys

docs = {
    'employee_wfh_policy.md': '# NovaTech Solutions Work-From-Home Policy\nEmployees are eligible for remote work 2 days a week pending manager approval. Please submit a request via the assistant.',
    'employee_leave_policy.md': '# NovaTech Solutions Leave Policy\nStandard annual leave is 20 days. Sick leave is unlimited. Submit requests to your manager.',
    'password_reset_policy.md': '# Password Reset Policy\nPasswords must be reset every 90 days. You can use the self-service portal or create an IT ticket if locked out.',
    'laptop_support_policy.md': '# Laptop Support Policy\nLaptops are replaced every 3 years. For immediate hardware or Wi-Fi issues, submit an IT support ticket.',
    'reimbursement_policy.md': '# Reimbursement Policy\nSubmit expenses within 30 days. WFH equipment allowance is $500 per year.',
    'employee_code_of_conduct.md': '# Code of Conduct\nTreat everyone with respect. Harassment will result in immediate escalation.'
}

def create_knowledge_files():
    os.makedirs('knowledge', exist_ok=True)
    for fname, content in docs.items():
        with open(f'knowledge/{fname}', 'w') as f:
            f.write(content)

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(Employee).first():
        users = [
            Employee(employee_id="EMP1001", name="Alice Admin", department="IT", email="alice@novatech.com", role="ADMIN", hashed_password="mock_hash_password"),
            Employee(employee_id="EMP1002", name="Bob Manager", department="Engineering", email="bob@novatech.com", role="MANAGER", hashed_password="mock_hash_password"),
            Employee(employee_id="EMP1024", name="Charlie Employee", department="Engineering", email="charlie@novatech.com", role="EMPLOYEE", manager="EMP1002", hashed_password="mock_hash_password"),
        ]
        db.add_all(users)
        db.commit()
    db.close()

if __name__ == "__main__":
    create_knowledge_files()
    seed_db()
    print("Database seeded and knowledge files created.")
