import React from 'react';
import PDFUpload from './PDFUpload';
import UploadDatabase from './UploadDatabase';

const DocumentManagement = () => {
  return (
    <div className="main-content">
      <div className="page-header">
        <h1>Document Management</h1>
        <p>Upload and manage medical documents and databases</p>
      </div>
      
      <div className="document-grid">
        <div className="document-section">
          <h2>PDF Documents</h2>
          <div className="card">
            <PDFUpload />
          </div>
        </div>
        
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
