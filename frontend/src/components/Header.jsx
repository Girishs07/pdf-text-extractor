import './Header.css';

function Header({ backendOnline }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">
            <span className="logo-icon">📄</span>
            <span className="logo-text">Text Extractor</span>
          </div>
        </div>

        <div className="header-right">
          <div className="status-badge">
            <span className={`status-dot ${backendOnline ? 'online' : 'offline'}`}></span>
            <span className="status-text">
              {backendOnline ? 'Backend Online' : 'Backend Offline'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
