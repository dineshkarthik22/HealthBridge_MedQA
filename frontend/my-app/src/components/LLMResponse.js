// src/components/LLMResponse.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../App.css';
const LLMResponse = ({ inputText }) => {
  const [response, setResponse] = useState('');

  useEffect(() => {
    const fetchResponse = async () => {
      if (inputText) {
        try {
          const res = await axios.post('https://api.example.com/query-llm', { input: inputText });
          setResponse(res.data.response);
        } catch (error) {
          console.error('Error fetching LLM response:', error);
        }
      }
    };

    fetchResponse();
  }, [inputText]);

  return (
    <div>
      <h3>LLM Response:</h3>
      <div className="recognized-text">
      <p>{response ? response : "No reponse yet. waiting..."}</p>
      </div>
    </div>
  );
};

export default LLMResponse;