// src/components/VoiceInputWithResponse.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.css';

const VoiceInputWithResponse = () => {
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTextSubmit = async (text) => {
    setInputText(text);
  };

  useEffect(() => {
    const fetchResponse = async () => {
      if (inputText) {
        setLoading(true);
        try {
          const res = await axios.post('https://api.example.com/query-llm', { input: inputText });
          setResponse(res.data.response);
        } catch (error) {
          console.error('Error fetching LLM response:', error);
          setResponse('Error fetching response.');
        } finally {
          setLoading(false);
        }
      } else {
        setResponse(''); 
      }
    };

    fetchResponse();
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
      <div className="recognized-text">
        <p>Input: {inputText || "No input yet."}</p>
      </div>
      <h3>LLM Response:</h3>
      <div className="recognized-text">
        {loading ? <p>Loading...</p> : <p>{response || "No response yet. Waiting..."}</p>}
      </div>
    </div>
  );
};

export default VoiceInputWithResponse;