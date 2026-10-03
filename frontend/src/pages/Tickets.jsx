
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
