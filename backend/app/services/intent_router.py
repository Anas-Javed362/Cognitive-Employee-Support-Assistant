from app.ai.providers.local import LocalLLMProvider

class IntentRouter:
    def __init__(self):
        self.llm = LocalLLMProvider()
        
    def route(self, message: str) -> str:
        msg_lower = message.lower()
        if "policy" in msg_lower or "password" in msg_lower or "reimbursement" in msg_lower:
            return "KNOWLEDGE_QUERY"
        elif "laptop" in msg_lower or "wi-fi" in msg_lower or "vpn" in msg_lower or "ticket" in msg_lower or "support" in msg_lower:
            return "IT_SUPPORT"
        elif "work from home" in msg_lower or "wfh" in msg_lower or "leave" in msg_lower:
            return "WFH_REQUEST"
        elif "delete" in msg_lower and "account" in msg_lower:
            return "HUMAN_ESCALATION"
        elif "status" in msg_lower and "ticket" in msg_lower:
            return "TICKET_STATUS"
        elif "status" in msg_lower and "request" in msg_lower:
            return "REQUEST_STATUS"
        return "UNKNOWN"
