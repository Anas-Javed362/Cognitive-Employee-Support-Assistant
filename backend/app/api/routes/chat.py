from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.intent_router import IntentRouter
from app.services.workflow_engine import WorkflowEngine
from app.rag.retrieval import RAGService
from app.ai.providers.local import LocalLLMProvider

router = APIRouter()
intent_router = IntentRouter()
workflow_engine = WorkflowEngine()
rag_service = RAGService()
llm_provider = LocalLLMProvider()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    intent = intent_router.route(request.message)
    
    if intent == "KNOWLEDGE_QUERY":
        rag_result = rag_service.query(request.message)
        context = rag_result.get("context", "")
        sources = rag_result.get("sources", [])
        
        prompt = f"Answer the user based on the context.\nContext: {context}\nQuestion: {request.message}"
        response_text = llm_provider.generate(prompt)
        
        if not context.strip():
            response_text = "I couldn't find enough information in the approved company knowledge base to answer that confidently. Would you like me to escalate this?"
            
        return ChatResponse(
            response=response_text,
            intent=intent,
            sources=sources,
            workflow_status="COMPLETED"
        )
        
    workflow_result = workflow_engine.execute(intent, {"message": request.message})
    
    return ChatResponse(
        response=workflow_result.get("message"),
        intent=intent,
        workflow_status=workflow_result.get("workflow_status")
    )
