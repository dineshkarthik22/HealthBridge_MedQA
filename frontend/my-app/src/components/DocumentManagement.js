import React from 'react';
import UploadDatabase from './UploadDatabase';

const DocumentManagement = () => {
  return (
    <div className="main-content">
      <div className="page-header">
        <h1>Document Management</h1>
        <p>Add documents to database by pasting any article from Cleveland Clinic</p>
      </div>
      
      <div className="document-grid">
        <div className="document-section">
          <h2>Database Management</h2>
          <div className="card">
            <UploadDatabase />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentManagement;
