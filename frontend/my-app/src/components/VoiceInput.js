// src/components/VoiceInput.js
import React, { useState } from 'react';
import '../App.css';
const VoiceInput = ({ onTextSubmit }) => {
  const [isListening, setIsListening] = useState(false);
  const [recognizedText, setRecognizedText] = useState(''); 

  const handleVoiceInput = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      const speechToText = event.results[0][0].transcript;
      setRecognizedText(speechToText); 
      onTextSubmit(speechToText); 
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      console.error('Error occurred in recognition:', event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  return (
    <div>
      <button onClick={handleVoiceInput} disabled={isListening}>
        {isListening ? 'Listening...' : 'Start Voice Input'}
      </button>
      {/* show text */}
      {recognizedText && (
        <div className="recognized-text">
          <h3>Recognized Text:</h3>
          <p>{recognizedText}</p>
        </div>
      )}
    </div>
  );
};

export default VoiceInput;