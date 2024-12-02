// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import PDFUpload from './components/PDFUpload';
import UploadDatabase from './components/UploadDatabase';
import VoiceInputWithResponse from './components/VoiceInputWithResponse';
import PatientPersonaForm from './components/PatientPersonaForm';
import './App.css';

const Home = () => (
  <div className="App">
    <header className="App-header">
      <h1>Medical Q&A</h1>
      
      <div className="component-container">
        <PDFUpload />
      </div>

      <div className="component-container">
        <UploadDatabase />
      </div>
      
      <div className="component-container">
        <VoiceInputWithResponse />
      </div>

      <div className="component-container">
        <Link to="/add-persona" className="add-persona-button">
          Add New Patient Persona
        </Link>
      </div>
    </header>
  </div>
);

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/add-persona" element={<PatientPersonaForm />} />
      </Routes>
    </Router>
  );
}

export default App;