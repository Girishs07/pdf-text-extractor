function HowItWorks({ onNavigate }) {
  const steps = [
    { number: '01', title: 'Choose a PDF', text: 'Select a PDF from your device or drag it into the upload area.' },
    { number: '02', title: 'We extract the text', text: 'The document is processed and its readable text is prepared for you.' },
    { number: '03', title: 'Review and download', text: 'Read the preview, check the details, and download the full text file.' },
  ];

  return (
    <section className="info-page how-page" aria-labelledby="how-title">
      <div className="info-eyebrow">HOW IT WORKS</div>
      <h1 id="how-title">From PDF to text in <span>three steps.</span></h1>
      <p className="info-lead">No learning curve. The whole process is designed to stay clear from upload to download.</p>

      <div className="steps-list">
        {steps.map((step) => (
          <article className="step-item" key={step.number}>
            <div className="step-number">{step.number}</div>
            <div>
              <h2>{step.title}</h2>
              <p>{step.text}</p>
            </div>
          </article>
        ))}
      </div>

      <button className="primary-action" type="button" onClick={() => onNavigate('home')}>Choose a PDF</button>
    </section>
  );
}

export default HowItWorks;
