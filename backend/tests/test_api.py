import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics_summary():
    response = client.get("/api/metrics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "open_tickets" in data
    assert "pending_requests" in data
    assert "open_escalations" in data


def test_chat_knowledge_query():
    response = client.post("/api/chat", json={"message": "What is the work-from-home policy?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "KNOWLEDGE_QUERY"
    assert data["response"] is not None


def test_chat_it_support():
    response = client.post("/api/chat", json={"message": "My laptop cannot connect to Wi-Fi"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "IT_SUPPORT"
    assert data["workflow_status"] == "COMPLETED"


def test_chat_wfh_request():
    response = client.post("/api/chat", json={"message": "I want to work from home tomorrow"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "WFH_REQUEST"
    assert data["workflow_status"] == "PENDING_APPROVAL"


def test_chat_escalation():
    response = client.post("/api/chat", json={"message": "Delete my employee account"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "HUMAN_ESCALATION"
    assert data["workflow_status"] == "ESCALATED"


def test_list_tickets():
    response = client.get("/api/tickets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_requests():
    response = client.get("/api/employee-requests/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_escalations():
    response = client.get("/api/escalations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_knowledge():
    response = client.get("/api/knowledge/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_ticket():
    response = client.post("/api/tickets/", json={
        "category": "HARDWARE",
        "issue": "Monitor flickering",
        "priority": "HIGH"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"].startswith("INC-")
    assert data["status"] == "OPEN"


def test_create_request():
    response = client.post("/api/employee-requests/", json={
        "request_type": "WFH",
        "date": "2026-10-04",
        "reason": "Doctor appointment"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["request_id"].startswith("REQ-")
    assert data["status"] == "PENDING_APPROVAL"


def test_create_escalation():
    response = client.post("/api/escalations/", json={
        "reason": "Account deletion",
        "conversation_context": "User requested account deletion",
        "requested_action": "DELETE_ACCOUNT",
        "priority": "HIGH"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["escalation_id"].startswith("ESC-")
    assert data["status"] == "OPEN"
