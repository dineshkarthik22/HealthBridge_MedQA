import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import '../App.css';

const Loader = () => (
  <div className="loader-container">
    <div className="loader">
      <div className="loader-ring"></div>
    </div>
    <p>Processing your question...</p>
  </div>
);

const VoiceInputWithResponse = () => {
  const [inputText, setInputText] = useState('');
  const [editableText, setEditableText] = useState('');
  const [response, setResponse] = useState('');
  const [evaluation, setEvaluation] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);

  const handleTextSubmit = (text) => {
    setInputText(text);
    setEditableText(text);
  };

  const handleSubmit = async () => {
    if (!editableText.trim()) {
      return;
    }
    
    setLoading(true);
    try {
      const requestBody = {
        patient_id: 1,
        query: editableText
      };

      const res = await axios.post('http://127.0.0.1:5000/query', requestBody);
      const { subquery, response: apiResponse, evaluation: apiEvaluation } = res.data.message[0];
      setResponse(apiResponse);
      setEvaluation(apiEvaluation);
    } catch (error) {
      console.error('Error fetching response:', error);
      setResponse('Error fetching response.');
      setEvaluation('');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (inputText) {
      setEditableText(inputText);
    }
  }, [inputText]);

  const startVoiceInput = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      const speechToText = event.results[0][0].transcript;
      handleTextSubmit(speechToText);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  return (
    <div className="page-container">
      <div className="input-section">
        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%'}}>
          <button 
              onClick={startVoiceInput} 
              className={`voice-button ${isListening ? 'listening' : ''}`}
              title="Start voice input"
              style={{marginTop: 'auto', marginBottom: '20px'}}
            >
              <svg 
                viewBox="0 0 24 24" 
                className="voice-icon"
                fill="none" 
                stroke="currentColor" 
                strokeWidth="2"
              >
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" y1="19" x2="12" y2="23" />
                <line x1="8" y1="23" x2="16" y2="23" />
              </svg>
              {isListening && <span className="pulse-ring"></span>}
            </button>
        </div>
        <div className="text-input-container">
          <textarea
            value={editableText}
            onChange={(e) => setEditableText(e.target.value)}
            placeholder="Type or speak your medical question here..."
            className="text-input"
          />
          <button onClick={handleSubmit} className="submit-button">
            Submit
          </button>
        </div>
      </div>

      <div className="content-section">
        {loading ? (
          <Loader />
        ) : (
          <>
            {response && (
              <div className="response-section">
                <h2>AI Response</h2>
                <div className="content-card">
                  <ReactMarkdown>
                    {response || ""}
                  </ReactMarkdown>
                </div>
              </div>
            )}

            {evaluation && (
              <div className="evaluation-section">
                <h2>Evaluation</h2>
                <div className="content-card">
                  <ReactMarkdown>
                    {evaluation || ""}
                  </ReactMarkdown>
                </div>
              </div>
            )}

            {!response && !evaluation && (
              <div className="empty-state">
                <p>Ask a question to see the response...</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default VoiceInputWithResponse;