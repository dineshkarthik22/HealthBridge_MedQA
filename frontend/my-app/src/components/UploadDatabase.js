import React, { useState } from 'react';
import axios from 'axios';

const UploadDatabase = () => {
  const [url, setUrl] = useState('');

  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const isValidUrl = (string) => {
    try {
      new URL(string);
      return true;
    } catch (error) {
      return false;
    }
  };

  const handleUpload = async () => {
    if (!url || !isValidUrl(url)) {
      alert('Please enter a valid URL.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/process-url', { 'database_url': url });
      alert(response.data.message); 
    } catch (error) {
      console.error('Error uploading database:', error);
      alert('Error uploading database.'); 
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Enter database URL"
        value={url}
        onChange={handleUrlChange}
      />
      <button onClick={handleUpload}>Submit URL</button>
    </div>
  );
};

export default UploadDatabase;