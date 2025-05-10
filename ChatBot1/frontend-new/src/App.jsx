import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import CVList from './CVList';
import UploadCV from './UploadCV';
import Chatbot from './Chatbot';
import './styles.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <h1>CV Chatbot</h1>
          <div className="nav-links">
            <NavLink 
              to="/" 
              className={({ isActive }) => isActive ? 'active' : ''}
              end
            >
              Home
            </NavLink>
            <NavLink 
              to="/upload" 
              className={({ isActive }) => isActive ? 'active' : ''}
            >
              Upload CV
            </NavLink>
            <NavLink 
              to="/chat" 
              className={({ isActive }) => isActive ? 'active' : ''}
            >
              Chat
            </NavLink>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<CVList />} />
            <Route path="/upload" element={<UploadCV />} />
            <Route path="/chat" element={<Chatbot />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;