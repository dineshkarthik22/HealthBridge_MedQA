import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.css';

const VoiceInputWithResponse = () => {
  const [inputText, setInputText] = useState('');
  const [editableText, setEditableText] = useState('');
  const [response, setResponse] = useState('');
  const [evaluation, setEvaluation] = useState(''); // 新增状态来存储 evaluation
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

      // 提取子查询、响应和评估
      const { subquery, response: apiResponse, evaluation: apiEvaluation } = res.data.message[0];
      setResponse(apiResponse); // 直接设置响应
      setEvaluation(apiEvaluation); // 设置评估
    } catch (error) {
      console.error('Error fetching response:', error);
      setResponse('Error fetching response.');
      setEvaluation(''); // 发生错误时清空评估
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
      <div className="response-container">
        {loading ? <p>Loading...</p> : <pre>{response || "No response yet. Waiting..."}</pre>}
      </div>
      <h3>Evaluation:</h3> {/* add evaluation*/}
      <div className="response-container">
        <pre>{evaluation || "No evaluation available."}</pre> {/* evaluation */}
      </div>
    </div>
  );
};

export default VoiceInputWithResponse;