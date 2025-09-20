import React from 'react';
import '../styles/LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loading-spinner">
      <div className="spinner-container">
        <div className="spinner-wrapper">
          <div className="spinner"></div>
          <div className="spinner-ring"></div>
        </div>
        <div className="loading-text">
          <h3>
            <span className="loading-icon">🤖</span>
            AI is analyzing your emotions...
          </h3>
          <p>Our advanced models are processing your input</p>
          <div className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;

