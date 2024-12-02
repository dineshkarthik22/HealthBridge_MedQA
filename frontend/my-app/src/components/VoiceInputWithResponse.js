import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.css';

const VoiceInputWithResponse = () => {
  const [inputText, setInputText] = useState('');
  const [editableText, setEditableText] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTextSubmit = (text) => {
    setInputText(text);
    setEditableText(text);
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const requestBody = {
        patient_id: 1,
        query: editableText
      };

      const res = await axios.post('http://127.0.0.1:5000/query', requestBody);

      
      const { subquery, response } = res.data.message[0]; 
      setResponse(`Subquery: ${subquery}\nResponse: ${response}`); 
    } catch (error) {
      console.error('Error fetching response:', error);
      setResponse('Error fetching response.');
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

    recognition.onresult = (event) => {
      const speechToText = event.results[0][0].transcript;
      handleTextSubmit(speechToText);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
    };

    recognition.onend = () => {
      console.log('Speech recognition ended.');
    };

    recognition.start();
  };

  return (
    <div>
      <h3>Voice Input</h3>
      <button onClick={startVoiceInput}>Start Voice Input</button>
      <div className="recognized-text centered-text">
        <h4>Input:</h4>
        <textarea
          value={editableText}
          onChange={(e) => setEditableText(e.target.value)}
          rows="4"
          cols="50"
        />
      </div>
      <button onClick={handleSubmit}>Submit</button>
      <h3>LLM Response:</h3>
      <div className="response-container"> {/* new CSS  */}
        {loading ? <p>Loading...</p> : <pre>{response || "No response yet. Waiting..."}</pre>}
      </div>
    </div>
  );
};

export default VoiceInputWithResponse;