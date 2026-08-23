function About({ onNavigate }) {
  return (
    <section className="info-page" aria-labelledby="about-title">
      <div className="info-eyebrow">ABOUT PDF TEXT EXTRACTOR</div>
      <h1 id="about-title">Turn your PDFs into <span>usable text.</span></h1>
      <p className="info-lead">A simple, focused tool for getting clean text from PDF documents without complicated setup or sign-ups.</p>

      <div className="info-card-grid">
        <article className="info-card">
          <div className="info-card-icon">✦</div>
          <h2>Simple by design</h2>
          <p>Drop in a PDF, let it process, and review the extracted text in one calm workspace.</p>
        </article>
        <article className="info-card">
          <div className="info-card-icon">♢</div>
          <h2>Private processing</h2>
          <p>Your document is processed for the task and is never saved as a permanent file.</p>
        </article>
        <article className="info-card">
          <div className="info-card-icon">ϟ</div>
          <h2>Built for speed</h2>
          <p>Get readable results quickly, whether you are checking a report or preparing notes.</p>
        </article>
      </div>

      <button className="primary-action" type="button" onClick={() => onNavigate('home')}>Start extracting</button>
    </section>
  );
}

export default About;
