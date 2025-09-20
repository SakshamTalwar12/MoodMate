import React, { useState } from 'react';
import '../styles/TextInput.css';

const TextInput = ({ onAnalysis, loading }) => {
  const [text, setText] = useState('');
  const [contentType, setContentType] = useState('movie');
  const [numRecommendations, setNumRecommendations] = useState(10);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onAnalysis(text.trim(), contentType, numRecommendations);
    }
  };

  const sampleTexts = [
    "I'm feeling really sad and lonely today",
    "I'm so excited and happy! This is amazing!",
    "I'm really angry about what happened",
    "I'm scared and worried about the future",
    "I feel neutral and calm today",
    "I'm feeling lazy and unmotivated"
  ];

  const handleSampleClick = (sampleText) => {
    setText(sampleText);
  };

  return (
    <div className="text-input">
      <div className="input-header">
        <div className="header-icon">📝</div>
        <h3>Text Emotion Analysis</h3>
        <p>Describe how you're feeling and get personalized movie recommendations powered by AI</p>
      </div>

      <form onSubmit={handleSubmit} className="text-form">
        <div className="form-group">
          <label htmlFor="text-input" className="form-label">
            <span className="label-icon">💭</span>
            How are you feeling?
          </label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Describe your current mood or feelings... (e.g., 'I'm feeling really excited about my vacation!')"
            className="text-area"
            rows="4"
            disabled={loading}
            required
          />
          <div className="char-count">{text.length}/500</div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="content-type" className="form-label">
              <span className="label-icon">🎬</span>
              Content Type
            </label>
            <select
              id="content-type"
              value={contentType}
              onChange={(e) => setContentType(e.target.value)}
              className="form-select"
              disabled={loading}
            >
              <option value="movie">🎬 Movies</option>
              <option value="tv_series">📺 TV Series</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="num-recommendations" className="form-label">
              <span className="label-icon">🔢</span>
              Recommendations
            </label>
            <select
              id="num-recommendations"
              value={numRecommendations}
              onChange={(e) => setNumRecommendations(parseInt(e.target.value))}
              className="form-select"
              disabled={loading}
            >
              <option value={5}>5 recommendations</option>
              <option value={10}>10 recommendations</option>
              <option value={15}>15 recommendations</option>
              <option value={20}>20 recommendations</option>
            </select>
          </div>
        </div>

        <button 
          type="submit" 
          className="submit-btn"
          disabled={loading || !text.trim()}
        >
          <span className="btn-icon">🚀</span>
          {loading ? 'Analyzing your emotions...' : 'Analyze Emotion & Get Recommendations'}
          <span className="btn-arrow">→</span>
        </button>
      </form>

      <div className="sample-texts">
        <h4>
          <span className="section-icon">💡</span>
          Try these sample texts:
        </h4>
        <div className="sample-grid">
          {sampleTexts.map((sample, index) => (
            <button
              key={index}
              className="sample-btn"
              onClick={() => handleSampleClick(sample)}
              disabled={loading}
            >
              <span className="sample-emoji">
                {index === 0 ? '😢' : index === 1 ? '😄' : index === 2 ? '😠' : 
                 index === 3 ? '😨' : index === 4 ? '😐' : '😴'}
              </span>
              {sample}
            </button>
          ))}
        </div>
      </div>

      <div className="info-box">
        <h4>
          <span className="section-icon">ℹ️</span>
          How it works:
        </h4>
        <div className="info-steps">
          <div className="step">
            <div className="step-number">1</div>
            <div className="step-content">
              <strong>AI Analysis</strong>
              <p>Our advanced AI analyzes your text to detect emotions like sadness, joy, anger, fear, etc.</p>
            </div>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <div className="step-content">
              <strong>Smart Matching</strong>
              <p>Based on your detected emotion, we recommend movies that perfectly match your mood</p>
            </div>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <div className="step-content">
              <strong>Hugging Face AI</strong>
              <p>We use cutting-edge Hugging Face models for the most accurate emotion detection</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TextInput;

