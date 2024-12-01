// src/components/UploadDatabase.js
import React, { useState } from 'react';
import axios from 'axios';

const UploadDatabase = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('database', file);

    try {
      const response = await axios.post('https://api.example.com/upload-database', formData);
      console.log(response.data);
    } catch (error) {
      console.error('Error uploading database:', error);
    }
  };

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload Database</button>
    </div>
  );
};

export default UploadDatabase;