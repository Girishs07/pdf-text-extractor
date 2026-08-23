import { useState, useRef } from 'react';
import './FileUploader.css';

function FileUploader({ onFileUpload, isLoading, uploadedFile }) {
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    if (allowedTypes.includes(file.type)) {
      onFileUpload(file);
    } else {
      alert('Please upload a PDF, DOCX, or TXT file');
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="file-uploader-section">
      <div
        className={`file-upload-area ${dragActive ? 'active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleChange}
          accept=".pdf,.docx,.txt"
          className="file-input"
          disabled={isLoading}
        />

        <div className="upload-content">
          <div className="upload-icon">⇧</div>
          <h3 className="upload-title">Drag &amp; Drop your PDF here</h3>
          <p className="upload-subtitle">or</p>
          <p className="upload-hint">PDF files only (max 100MB)</p>
          
          <button
            className="upload-button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading}
            type="button"
          >
            {isLoading ? 'Processing...' : 'Choose PDF File'}
          </button>
          <p className="upload-security"><span aria-hidden="true">♙</span> Your files are secure and never stored.</p>
        </div>
      </div>

      {uploadedFile && !isLoading && (
        <div className="file-info-card">
          <div className="file-info-header">
            <span className="file-icon">📄</span>
            <div className="file-details">
              <h4 className="file-name">{uploadedFile.name}</h4>
              <p className="file-meta">{formatFileSize(uploadedFile.size)}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default FileUploader;
