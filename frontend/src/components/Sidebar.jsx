import './Sidebar.css';

function Sidebar({ backendOnline }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-content">
        <div className="sidebar-section">
          <h3 className="sidebar-title">✨ Features</h3>
          <ul className="sidebar-list">
            <li>🚀 Fast Processing</li>
            <li>📊 Multiple Formats</li>
            <li>📈 File Statistics</li>
            <li>💾 Download Results</li>
            <li>🔒 Secure Processing</li>
          </ul>
        </div>

        <div className="sidebar-divider"></div>

        <div className="sidebar-section">
          <h3 className="sidebar-title">💡 Tips</h3>
          <ul className="sidebar-list">
            <li>📄 PDF: Text-based PDFs work best</li>
            <li>📦 Size: Keep under 100MB</li>
            <li>🌐 Network: Good connection recommended</li>
            <li>🔄 Retry: Wait 30s if error occurs</li>
          </ul>
        </div>

        <div className="sidebar-divider"></div>

        <div className="sidebar-section">
          <h3 className="sidebar-title">📝 Supported Formats</h3>
          <div className="format-badges">
            <span className="format-badge">PDF</span>
            <span className="format-badge">DOCX</span>
            <span className="format-badge">TXT</span>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
