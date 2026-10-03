# Demo Scenarios

Run these scenarios in the AI Assistant chat interface.

### DEMO 1: Knowledge Query
**User:** "What is the work-from-home policy?"
**Expected:** The system performs intent routing, queries the FAISS vector database, returns the chunked markdown context, and formulates a policy-grounded answer (with `employee_wfh_policy.md` cited as a source).

### DEMO 2: IT Support Ticket Automation
**User:** "My laptop cannot connect to Wi-Fi."
**Expected:** The intent router detects `IT_SUPPORT`. The workflow engine automatically provisions an IT incident ticket.
**Result:** Returns a ticket ID like `INC-XXXXXXXX` and updates the Dashboard "Open Tickets" count.

### DEMO 3: Employee HR Request
**User:** "I want to work from home tomorrow."
**Expected:** The system identifies a `WFH_REQUEST`. It executes the employee request workflow.
**Result:** Returns a request ID like `REQ-XXXXXXXX` with status `PENDING_APPROVAL`.

### DEMO 4: Human Escalation
**User:** "Delete my employee account."
**Expected:** Identifies the high-risk action (`HUMAN_ESCALATION`) and halts automatic processing.
**Result:** Esculates the request to human HR/IT support. 

### DEMO 5: System Resilience and Fallback
If IBM watsonx credentials (`WATSONX_API_KEY`) are missing from `.env`, the system automatically switches to the `LocalLLMProvider` and `RuleBasedIntentRouter`, guaranteeing the demo works on local machines without cloud configuration.
