
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
                assistantContent += '\n\nSources: ' + data.sources.join(', ');
            }
            if (data.intent === 'IT_SUPPORT' || data.intent === 'WFH_REQUEST') {
                assistantContent += '\nStatus: ' + data.workflow_status;
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
