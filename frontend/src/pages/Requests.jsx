
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
