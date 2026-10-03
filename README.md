# Cognitive Employee Support & Process Automation Assistant

An enterprise-style employee support assistant built with **FastAPI and React**. The system handles employee knowledge and policy questions through RAG, creates IT support tickets, processes HR requests such as WFH requests, and supports human-in-the-loop escalation.

## Architecture

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn

### Frontend

* React
* Vite
* React Router
* Vanilla CSS

### AI and RAG

* LangChain
* FAISS
* Sentence Transformers
* Local development fallback

### Integrations

* IBM watsonx.ai
* Deterministic local fallback when IBM credentials are unavailable

## Features

* Knowledge and policy question answering using RAG
* Local FAISS-based document retrieval
* IT support ticket creation and tracking
* HR request processing, including WFH requests
* Human-in-the-loop escalation
* React-based employee dashboard
* Chat interface
* Local AI fallback without external API credentials
* SQLite database for local development

## Project Setup

### 1. Backend

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.\.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
python scripts/seed_database.py
```

Ingest the knowledge base:

```bash
python scripts/ingest_knowledge.py
```

Start the backend:

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 2. Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server will provide the frontend URL in the terminal.

## IBM watsonx Configuration

To enable IBM watsonx.ai, create a `.env` file in the project root:

```env
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=your_url
WATSONX_MODEL_ID=meta-llama/llama-3-70b-instruct
```

If these credentials are not configured, the application automatically uses the local development fallback.

## Local Development Mode

The application can operate without IBM credentials using:

* Rule-based intent routing
* Local FAISS vector search
* Sentence Transformers
* Context-based fallback responses
* SQLite database
* React frontend

This allows the complete application workflow to be tested locally without external AI services.

## Docker

To run the application using Docker:

```bash
docker-compose up --build
```

## Project Structure

```text
Cognitive-Employee-Support-Assistant/
│
├── backend/
│   └── app/
│
├── frontend/
│
├── scripts/
│   ├── seed_database.py
│   └── ingest_knowledge.py
│
├── requirements.txt
├── docker-compose.yml
├── .env
└── README.md
```

## Known Limitations

* SQLite is currently used as the default database.
* Production deployment should use PostgreSQL.
* Frontend authentication currently requires further implementation.
* IBM watsonx Assistant integration is planned.
* IBM watsonx Orchestrate integration is planned for complex background workflows.

## Future Improvements

* PostgreSQL production database
* OAuth2/JWT authentication
* IBM watsonx Assistant integration
* IBM watsonx Orchestrate integration
* Additional enterprise workflow integrations
* Production deployment and monitoring

## License

This project is available under the MIT License.
