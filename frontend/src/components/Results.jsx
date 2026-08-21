import { useState } from 'react';
import './Results.css';

function Results({ text, onDownload, uploadedFile }) {
  const [previewLength, setPreviewLength] = useState(500);

  const words = text.split(/\s+/).filter(word => word.length > 0);
  const lines = text.split('\n');
  const paragraphs = text.split('\n\n').filter(p => p.trim().length > 0);

  const stats = [
    { label: '📝 Characters', value: text.length.toLocaleString() },
    { label: '📊 Words', value: words.length.toLocaleString() },
    { label: '📄 Lines', value: lines.length.toLocaleString() },
    { label: '📋 Paragraphs', value: paragraphs.length.toLocaleString() },
  ];

  const preview = text.length > previewLength 
    ? text.substring(0, previewLength) + '...' 
    : text;

  return (
    <div className="results-section">
      <h2 className="section-title">📖 Results</h2>

      {/* Statistics Cards */}
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card">
            <p className="stat-label">{stat.label}</p>
            <p className="stat-value">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Text Preview */}
      <div className="preview-section">
        <div className="preview-header">
          <h3 className="preview-title">👀 Text Preview</h3>
          <div className="preview-controls">
            <label htmlFor="preview-slider" className="slider-label">
              Length: {previewLength.toLocaleString()} characters
            </label>
            <input
              id="preview-slider"
              type="range"
              min="100"
              max={Math.min(2000, text.length)}
              value={previewLength}
              onChange={(e) => setPreviewLength(Number(e.target.value))}
              className="slider"
            />
          </div>
        </div>

        <div className="text-preview">
          {preview}
        </div>
      </div>

      {/* Download Section */}
      <div className="download-section">
        <div className="download-info">
          <h3 className="download-title">📥 Download</h3>
          <p className="download-subtitle">
            Ready to download your extracted text?
          </p>
          <p className="download-detail">
            Full text contains {text.length.toLocaleString()} characters from {uploadedFile?.name}
          </p>
        </div>

        <button className="download-button" onClick={onDownload}>
          <span>📥 Download Full Text</span>
          <span className="file-format">.txt</span>
        </button>
      </div>
    </div>
  );
}

export default Results;
