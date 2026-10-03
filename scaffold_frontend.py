import os

src_code = {
    'index.css': '''
:root {
    --bg-color: #0f172a;
    --text-color: #f8fafc;
    --primary: #3b82f6;
    --primary-hover: #2563eb;
    --secondary: #1e293b;
    --border: #334155;
    --success: #10b981;
    --error: #ef4444;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.5;
}

.app-container {
    display: flex;
    height: 100vh;
}

.sidebar {
    width: 250px;
    background-color: var(--secondary);
    border-right: 1px solid var(--border);
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.sidebar h2 {
    color: var(--primary);
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.nav-link {
    color: var(--text-color);
    text-decoration: none;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    transition: all 0.2s;
}

.nav-link:hover, .nav-link.active {
    background-color: var(--primary);
    color: white;
}

.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 2rem;
    overflow-y: auto;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.card {
    background-color: var(--secondary);
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    padding: 1.5rem;
}

.card h3 {
    color: #94a3b8;
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}

.card .value {
    font-size: 2rem;
    font-weight: bold;
}

.chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    background-color: var(--secondary);
    border-radius: 0.5rem;
    border: 1px solid var(--border);
    overflow: hidden;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.message {
    max-width: 80%;
    padding: 1rem;
    border-radius: 0.5rem;
}

.message.user {
    align-self: flex-end;
    background-color: var(--primary);
}

.message.assistant {
    align-self: flex-start;
    background-color: var(--bg-color);
    border: 1px solid var(--border);
}

.chat-input-container {
    padding: 1rem;
    border-top: 1px solid var(--border);
    display: flex;
    gap: 1rem;
}

.chat-input-container input {
    flex: 1;
    background-color: var(--bg-color);
    border: 1px solid var(--border);
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    outline: none;
}

.chat-input-container input:focus {
    border-color: var(--primary);
}

.chat-input-container button {
    background-color: var(--primary);
    color: white;
    border: none;
    padding: 0 1.5rem;
    border-radius: 0.5rem;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.2s;
}

.chat-input-container button:hover {
    background-color: var(--primary-hover);
}

.table-container {
    background-color: var(--secondary);
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    overflow: hidden;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

th {
    background-color: rgba(0,0,0,0.2);
    color: #94a3b8;
    font-weight: 500;
}

.status-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: bold;
}

.status-OPEN, .status-PENDING_APPROVAL {
    background-color: rgba(239, 68, 68, 0.2);
    color: #ef4444;
}

.status-COMPLETED, .status-RESOLVED {
    background-color: rgba(16, 185, 129, 0.2);
    color: #10b981;
}
''',
    'App.jsx': '''
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Chat from './pages/Chat';
import Tickets from './pages/Tickets';
import Requests from './pages/Requests';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <nav className="sidebar">
          <h2>Cognitive Support</h2>
          <Link to="/" className="nav-link">Dashboard</Link>
          <Link to="/chat" className="nav-link">AI Assistant</Link>
          <Link to="/tickets" className="nav-link">IT Tickets</Link>
          <Link to="/requests" className="nav-link">HR Requests</Link>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/tickets" element={<Tickets />} />
            <Route path="/requests" element={<Requests />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
''',
    'main.jsx': '''
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
'''
}

pages_code = {
    'Dashboard.jsx': '''
import React, { useEffect, useState } from 'react';

export default function Dashboard() {
    const [stats, setStats] = useState({ tickets: 0, requests: 0 });

    useEffect(() => {
        // Mock fetch
        setStats({ tickets: 5, requests: 2 });
    }, []);

    return (
        <div>
            <h1 style={{marginBottom: "2rem"}}>Dashboard</h1>
            <div className="dashboard-grid">
                <div className="card">
                    <h3>Open Tickets</h3>
                    <div className="value">{stats.tickets}</div>
                </div>
                <div className="card">
                    <h3>Pending Requests</h3>
                    <div className="value">{stats.requests}</div>
                </div>
                <div className="card">
                    <h3>System Health</h3>
                    <div className="value" style={{color: "var(--success)"}}>Online</div>
                </div>
            </div>
        </div>
    )
}
''',
    'Chat.jsx': '''
import React, { useState } from 'react';

export default function Chat() {
    const [messages, setMessages] = useState([{role: 'assistant', content: 'Hello! I am your Cognitive Employee Support Assistant. How can I help you today?'}]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;
        
        const userMsg = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setLoading(true);
        
        try {
            const res = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMsg.content, history: messages })
            });
            const data = await res.json();
            
            let assistantContent = data.response;
            if (data.sources && data.sources.length > 0) {
                assistantContent += '\\n\\nSources: ' + data.sources.join(', ');
            }
            if (data.intent === 'IT_SUPPORT' || data.intent === 'WFH_REQUEST') {
                assistantContent += '\\nStatus: ' + data.workflow_status;
            }
            
            setMessages(prev => [...prev, { role: 'assistant', content: assistantContent }]);
        } catch (err) {
            setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error connecting to the server.' }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{height: "100%"}}>
            <h1 style={{marginBottom: "1rem"}}>AI Assistant</h1>
            <div className="chat-container">
                <div className="chat-messages">
                    {messages.map((m, i) => (
                        <div key={i} className={`message ${m.role}`} style={{whiteSpace: "pre-wrap"}}>
                            {m.content}
                        </div>
                    ))}
                    {loading && <div className="message assistant">Thinking...</div>}
                </div>
                <form className="chat-input-container" onSubmit={sendMessage}>
                    <input 
                        value={input} 
                        onChange={e => setInput(e.target.value)} 
                        placeholder="Ask about policies, create IT tickets, or request leave..."
                    />
                    <button type="submit">Send</button>
                </form>
            </div>
        </div>
    )
}
''',
    'Tickets.jsx': '''
import React, { useEffect, useState } from 'react';

export default function Tickets() {
    const [tickets, setTickets] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/tickets/')
            .then(r => r.json())
            .then(data => setTickets(data))
            .catch(e => console.error(e));
    }, []);

    return (
        <div>
            <h1 style={{marginBottom: "2rem"}}>IT Tickets</h1>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Category</th>
                            <th>Issue</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tickets.map(t => (
                            <tr key={t.ticket_id}>
                                <td>{t.ticket_id}</td>
                                <td>{t.category}</td>
                                <td>{t.issue}</td>
                                <td><span className={`status-badge status-${t.status}`}>{t.status}</span></td>
                            </tr>
                        ))}
                        {tickets.length === 0 && <tr><td colSpan="4">No tickets found.</td></tr>}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
''',
    'Requests.jsx': '''
import React, { useEffect, useState } from 'react';

export default function Requests() {
    const [requests, setRequests] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/api/employee-requests/')
            .then(r => r.json())
            .then(data => setRequests(data))
            .catch(e => console.error(e));
    }, []);

    return (
        <div>
            <h1 style={{marginBottom: "2rem"}}>HR Requests</h1>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Type</th>
                            <th>Reason</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {requests.map(r => (
                            <tr key={r.request_id}>
                                <td>{r.request_id}</td>
                                <td>{r.request_type}</td>
                                <td>{r.reason}</td>
                                <td><span className={`status-badge status-${r.status}`}>{r.status}</span></td>
                            </tr>
                        ))}
                        {requests.length === 0 && <tr><td colSpan="4">No requests found.</td></tr>}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
'''
}

os.makedirs('frontend/src/pages', exist_ok=True)
for fname, content in src_code.items():
    with open(f'frontend/src/{fname}', 'w') as f:
        f.write(content)

for fname, content in pages_code.items():
    with open(f'frontend/src/pages/{fname}', 'w') as f:
        f.write(content)
