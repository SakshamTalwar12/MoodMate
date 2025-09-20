import React from 'react';
import '../styles/ResultsSection.css';

const ResultsSection = ({ results }) => {
  if (!results) return null;

  const { emotion_analysis, recommendations, content_type, num_recommendations } = results;

  const getEmotionIcon = (emotion) => {
    const emotionIcons = {
      'Sad': '😢',
      'Happy/Joy': '😊',
      'Love/Surprise': '😍',
      'Angry': '😠',
      'Fear': '😨',
      'Lazy/Disgust': '😴',
      'Neutral': '😐'
    };
    return emotionIcons[emotion] || '😊';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'high';
    if (confidence >= 0.6) return 'medium';
    return 'low';
  };

  return (
    <section className="results-section">
      <div className="results-container">
        <h2 className="results-title">🎬 Your Personalized Recommendations</h2>
        
        {/* Emotion Analysis Results */}
        <div className="emotion-analysis">
          <h3>🎭 Detected Emotion</h3>
          <div className="emotion-card">
            <div className="emotion-main">
              <span className="emotion-icon">
                {getEmotionIcon(emotion_analysis.emotion_label)}
              </span>
              <div className="emotion-details">
                <h4 className="emotion-name">{emotion_analysis.emotion_label}</h4>
                <div className="confidence-meter">
                  <span className="confidence-label">Confidence:</span>
                  <div className={`confidence-bar ${getConfidenceColor(emotion_analysis.confidence)}`}>
                    <div 
                      className="confidence-fill"
                      style={{ width: `${emotion_analysis.confidence * 100}%` }}
                    ></div>
                  </div>
                  <span className="confidence-value">
                    {(emotion_analysis.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
            
            {emotion_analysis.individual_results && (
              <div className="individual-results">
                <h5>Individual Analysis Results:</h5>
                <div className="individual-grid">
                  {emotion_analysis.individual_results.map((result, index) => (
                    <div key={index} className="individual-result">
                      <span className="method">{result.method}</span>
                      <span className="emotion">{result.emotion_label}</span>
                      <span className="confidence">
                        {(result.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Recommendations */}
        <div className="recommendations">
          <h3>
            🎬 Top {num_recommendations} {content_type === 'movie' ? 'Movies' : 'TV Series'} 
            for Your Mood
          </h3>
          
          {recommendations && recommendations.length > 0 ? (
            <div className="recommendations-grid">
              {recommendations.map((movie, index) => (
                <div key={index} className="movie-card">
                  <div className="movie-header">
                    <h4 className="movie-title">{movie.title}</h4>
                    <div className="movie-rating">
                      <span className="rating-value">{movie.rating}</span>
                      <span className="rating-star">⭐</span>
                    </div>
                  </div>
                  
                  <div className="movie-details">
                    <div className="movie-year">
                      <span className="year-label">Year:</span>
                      <span className="year-value">{movie.year}</span>
                    </div>
                    
                    {movie.genres && (
                      <div className="movie-genres">
                        <span className="genres-label">Genres:</span>
                        <div className="genres-list">
                          {movie.genres.map((genre, genreIndex) => (
                            <span key={genreIndex} className="genre-tag">
                              {genre}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  
                  {movie.overview && (
                    <div className="movie-overview">
                      <p>{movie.overview}</p>
                    </div>
                  )}
                  
                  <div className="movie-rank">
                    <span className="rank-number">#{index + 1}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-recommendations">
              <p>No recommendations available for your current emotion.</p>
            </div>
          )}
        </div>

        {/* Analysis Summary */}
        <div className="analysis-summary">
          <h3>📊 Analysis Summary</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <span className="summary-label">Analysis Method:</span>
              <span className="summary-value">{emotion_analysis.method}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Content Type:</span>
              <span className="summary-value">
                {content_type === 'movie' ? 'Movies' : 'TV Series'}
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Recommendations:</span>
              <span className="summary-value">{num_recommendations}</span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Confidence:</span>
              <span className="summary-value">
                {(emotion_analysis.confidence * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ResultsSection;








