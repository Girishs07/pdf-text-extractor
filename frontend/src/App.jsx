import { useState, useEffect } from 'react';
import './App.css';
import FileUploader from './components/FileUploader';
import Results from './components/Results';
import Sidebar from './components/Sidebar';
import Header from './components/Header';

const BACKEND_URL = 'https://pdf-textextractor.onrender.com';

function App() {
  const [extractedText, setExtractedText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [backendOnline, setBackendOnline] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Check backend status on mount
  useEffect(() => {
    checkBackendStatus();
    const interval = setInterval(checkBackendStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/health`, { timeout: 5000 });
      setBackendOnline(response.status === 200);
    } catch {
      setBackendOnline(false);
    }
  };

  const handleFileUpload = async (file) => {
    setError('');
    setSuccess('');
    setExtractedText('');
    setUploadedFile(file);

    const fileSizeMB = file.size / (1024 * 1024);

    // Validation
    if (fileSizeMB > 100) {
      setError(`❌ File too large: ${fileSizeMB.toFixed(1)}MB. Maximum allowed: 100MB`);
      return;
    }

    if (file.type === 'application/pdf' && !backendOnline) {
      setError('❌ Cannot process PDF: Backend service is offline');
      return;
    }

    setIsLoading(true);

    try {
      let text = '';

      if (file.type === 'application/pdf') {
        text = await extractPdfViaAPI(file);
      } else if (file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        text = await extractDocxText(file);
      } else if (file.type === 'text/plain') {
        text = await extractTxtText(file);
      } else {
        setError('❌ Unsupported file type! Please upload a PDF, DOCX, or TXT file.');
        setIsLoading(false);
        return;
      }

      if (text && text.trim()) {
        setExtractedText(text);
        setSuccess(`✅ Success! Extracted ${text.length.toLocaleString()} characters`);
      } else {
        setError('⚠️ No text content found in the uploaded file.');
      }
    } catch (err) {
      setError(`🚫 Error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const extractPdfViaAPI = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${BACKEND_URL}/extract-pdf`, {
        method: 'POST',
        body: formData,
        signal: AbortSignal.timeout(300000),
      });

      if (response.status === 200) {
        const result = await response.json();
        return result.extracted_text || '';
      } else if (response.status === 413) {
        throw new Error('File too large - Please use a smaller PDF file (max 100MB)');
      } else if (response.status === 400) {
        const error = await response.json();
        throw new Error(`Invalid file: ${error.detail || 'Invalid PDF'}`);
      } else if (response.status === 500) {
        throw new Error('Server error - There was an issue processing your PDF. Please try again.');
      } else {
        const error = await response.json();
        throw new Error(error.detail || 'API Error');
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        throw new Error('Request timed out - The PDF might be too large or complex.');
      }
      throw err;
    }
  };

  const extractDocxText = async (file) => {
    // For DOCX files, we need to parse them client-side
    // This is a simplified version - for production, consider using a library
    throw new Error('DOCX extraction requires backend support. Ensure backend is online.');
  };

  const extractTxtText = async (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = () => reject(new Error('Failed to read TXT file'));
      reader.readAsText(file);
    });
  };

  const downloadText = () => {
    const element = document.createElement('a');
    const file = new Blob([extractedText], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `extracted_${uploadedFile?.name || 'text'}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="app">
      <Header backendOnline={backendOnline} />
      
      <div className="app-container">
        <Sidebar backendOnline={backendOnline} />
        
        <main className="main-content">
          <FileUploader 
            onFileUpload={handleFileUpload} 
            isLoading={isLoading}
            uploadedFile={uploadedFile}
          />

          {error && (
            <div className="alert alert-error">
              {error}
            </div>
          )}

          {success && (
            <div className="alert alert-success">
              {success}
            </div>
          )}

          {extractedText && (
            <Results 
              text={extractedText} 
              onDownload={downloadText}
              uploadedFile={uploadedFile}
            />
          )}

          {isLoading && (
            <div className="loading-container">
              <div className="spinner"></div>
              <p className="loading-text">Processing your file...</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
