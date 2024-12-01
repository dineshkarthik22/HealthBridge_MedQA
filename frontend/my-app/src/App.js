// src/App.js
import React, { useState } from 'react';
import PDFUpload from './components/PDFUpload';
import UploadDatabase from './components/UploadDatabase';
import VoiceInputWithResponse from './components/VoiceInputWithResponse';
import './App.css'; 

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <h1> Medical Q&A</h1>
        
        <div className="component-container">
          <PDFUpload />
        </div>

        <div className="component-container">
          <UploadDatabase />
        </div>
        
        <div className="component-container">
          <VoiceInputWithResponse />
        </div>
      </header>
    </div>
  );
}

export default App;