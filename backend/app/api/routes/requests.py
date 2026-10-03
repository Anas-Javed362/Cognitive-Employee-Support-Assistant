from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.request import EmployeeRequest
from app.schemas.request import EmployeeRequestCreate, EmployeeRequest as RequestSchema
import uuid
from typing import List

router = APIRouter()

@router.post("/", response_model=RequestSchema)
def create_request(req: EmployeeRequestCreate, db: Session = Depends(get_db)):
    db_req = EmployeeRequest(
        request_id=f"REQ-{str(uuid.uuid4())[:8].upper()}",
        employee_id="EMP1024",
        request_type=req.request_type,
        date=req.date,
        reason=req.reason
    )
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

@router.get("/{request_id}", response_model=RequestSchema)
def get_request(request_id: str, db: Session = Depends(get_db)):
    req = db.query(EmployeeRequest).filter(EmployeeRequest.request_id == request_id).first()
    if req is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return req

@router.get("/", response_model=List[RequestSchema])
def list_requests(db: Session = Depends(get_db)):
    return db.query(EmployeeRequest).all()
