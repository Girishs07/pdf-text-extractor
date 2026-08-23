import './Header.css';

function Header({ backendOnline, activePage, onNavigate }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">
            <span className="logo-icon">▤</span>
            <span className="logo-text">PDF Text Extractor</span>
          </div>
        </div>

        <nav className="nav-links" aria-label="Main navigation">
          <button className={`nav-link ${activePage === 'home' ? 'active' : ''}`} type="button" onClick={() => onNavigate('home')}>Home</button>
          <button className={`nav-link ${activePage === 'about' ? 'active' : ''}`} type="button" onClick={() => onNavigate('about')}>About</button>
          <button className={`nav-link ${activePage === 'how' ? 'active' : ''}`} type="button" onClick={() => onNavigate('how')}>How it Works</button>
        </nav>

        <div className="header-right">
          <a className="github-button" href="https://github.com/Girishs07/pdf-text-extractor" target="_blank" rel="noreferrer">
            <span aria-hidden="true">●</span> View on GitHub
          </a>
        </div>
      </div>
    </header>
  );
}

export default Header;
