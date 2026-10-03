
import React, { useEffect, useState } from 'react';

export default function Dashboard() {
    const [stats, setStats] = useState({ open_tickets: 0, pending_requests: 0, open_escalations: 0, total_tickets: 0, total_requests: 0 });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://localhost:8000/api/metrics/summary')
            .then(r => r.json())
            .then(data => {
                setStats(data);
                setLoading(false);
            })
            .catch(e => {
                console.error(e);
                setLoading(false);
            });
    }, []);

    return (
        <div>
            <h1 style={{marginBottom: "2rem"}}>Dashboard</h1>
            {loading ? (
                <p style={{color: "#94a3b8"}}>Loading metrics...</p>
            ) : (
                <div className="dashboard-grid">
                    <div className="card">
                        <h3>Open Tickets</h3>
                        <div className="value">{stats.open_tickets}</div>
                        <p style={{color: "#94a3b8", fontSize: "0.8rem", marginTop: "0.5rem"}}>{stats.total_tickets} total</p>
                    </div>
                    <div className="card">
                        <h3>Pending Requests</h3>
                        <div className="value">{stats.pending_requests}</div>
                        <p style={{color: "#94a3b8", fontSize: "0.8rem", marginTop: "0.5rem"}}>{stats.total_requests} total</p>
                    </div>
                    <div className="card">
                        <h3>Open Escalations</h3>
                        <div className="value" style={{color: stats.open_escalations > 0 ? "var(--error)" : "var(--text-color)"}}>{stats.open_escalations}</div>
                    </div>
                    <div className="card">
                        <h3>System Health</h3>
                        <div className="value" style={{color: "var(--success)"}}>Online</div>
                    </div>
                </div>
            )}
        </div>
    )
}
