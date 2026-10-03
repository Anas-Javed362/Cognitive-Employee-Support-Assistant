from app.db.database import SessionLocal
from app.models.ticket import Ticket
from app.models.request import EmployeeRequest
from app.models.escalation import Escalation
import uuid
from datetime import date

class WorkflowEngine:
    def __init__(self, db_session=None):
        self.db = db_session
        
    def _get_db(self):
        if self.db:
            return self.db
        return SessionLocal()
    
    def _close_db(self, db):
        if not self.db:
            db.close()
        
    def execute(self, intent: str, context: dict):
        if intent == "IT_SUPPORT":
            return self._create_ticket(context)
        elif intent == "WFH_REQUEST":
            return self._create_wfh_request(context)
        elif intent == "HUMAN_ESCALATION":
            return self._create_escalation(context)
        elif intent == "KNOWLEDGE_QUERY":
            return {"status": "SUCCESS", "message": "Knowledge retrieved.", "workflow_status": "COMPLETED"}
        
        return {"status": "FAILED", "message": "I'm not sure how to help with that. Could you rephrase or provide more details?", "workflow_status": "FAILED"}
    
    def _create_ticket(self, context: dict):
        db = self._get_db()
        try:
            ticket_id = f"INC-{str(uuid.uuid4())[:8].upper()}"
            db_ticket = Ticket(
                ticket_id=ticket_id,
                employee_id="EMP1024",
                category="IT_SUPPORT",
                issue=context.get("message", "IT support request"),
                priority="MEDIUM",
                status="OPEN",
                assigned_team="IT Help Desk"
            )
            db.add(db_ticket)
            db.commit()
            return {
                "status": "SUCCESS",
                "message": f"IT support ticket **{ticket_id}** has been created and assigned to the IT Help Desk. You can track its status on the Tickets page.",
                "workflow_status": "COMPLETED",
                "ticket_id": ticket_id
            }
        except Exception as e:
            db.rollback()
            return {"status": "FAILED", "message": f"Failed to create ticket: {e}", "workflow_status": "FAILED"}
        finally:
            self._close_db(db)
    
    def _create_wfh_request(self, context: dict):
        db = self._get_db()
        try:
            request_id = f"REQ-{str(uuid.uuid4())[:8].upper()}"
            db_req = EmployeeRequest(
                request_id=request_id,
                employee_id="EMP1024",
                request_type="WFH",
                date=str(date.today()),
                reason=context.get("message", "Work from home request"),
                status="PENDING_APPROVAL",
                approver="EMP1002"
            )
            db.add(db_req)
            db.commit()
            return {
                "status": "SUCCESS",
                "message": f"Work-from-home request **{request_id}** has been submitted and is pending manager approval. You can track it on the HR Requests page.",
                "workflow_status": "PENDING_APPROVAL",
                "request_id": request_id
            }
        except Exception as e:
            db.rollback()
            return {"status": "FAILED", "message": f"Failed to create request: {e}", "workflow_status": "FAILED"}
        finally:
            self._close_db(db)
    
    def _create_escalation(self, context: dict):
        db = self._get_db()
        try:
            escalation_id = f"ESC-{str(uuid.uuid4())[:8].upper()}"
            db_esc = Escalation(
                escalation_id=escalation_id,
                employee_id="EMP1024",
                reason="High-risk action requiring human approval",
                conversation_context=context.get("message", ""),
                requested_action=context.get("message", "Account deletion request"),
                priority="HIGH",
                status="OPEN"
            )
            db.add(db_esc)
            db.commit()
            return {
                "status": "ESCALATED",
                "message": f"This request requires human approval. Escalation **{escalation_id}** has been created and assigned to HR/IT management for review.",
                "workflow_status": "ESCALATED",
                "escalation_id": escalation_id
            }
        except Exception as e:
            db.rollback()
            return {"status": "FAILED", "message": f"Failed to create escalation: {e}", "workflow_status": "FAILED"}
        finally:
            self._close_db(db)
