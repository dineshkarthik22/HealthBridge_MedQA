// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import VoiceInputWithResponse from './components/VoiceInputWithResponse';
import PatientPersonaForm from './components/PatientPersonaForm';
import DocumentManagement from './components/DocumentManagement';
import './App.css';

const Navigation = () => (
  <nav className="main-nav">
    <div className="nav-brand">
      <h2>HealthBridge MedQA</h2>
    </div>
    <div className="nav-links">
      <NavLink to="/" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"} end>
        Home
      </NavLink>
      <NavLink to="/documents" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
        Documents
      </NavLink>
      <NavLink to="/add-persona" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
        Add Patient
      </NavLink>
    </div>
  </nav>
);

const Home = () => (
  <div className="App">
    <div className="main-content">
      <div className="page-header">
        <h1>Medical Q&A Interface</h1>
        <p>Ask questions and get AI-powered medical insights</p>
      </div>
      <div className="qa-section">
        <div className="card main-qa-card">
          <VoiceInputWithResponse />
        </div>
      </div>
    </div>
  </div>
);

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/documents" element={<DocumentManagement />} />
          <Route path="/add-persona" element={<PatientPersonaForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;