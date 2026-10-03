
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
