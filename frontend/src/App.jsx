import React, { useState, useEffect } from 'react';
import './styles/App.css';
import Header from './components/Header';
import InputSection from './components/InputSection';
import ResultsSection from './components/ResultsSection';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('text');

  // Convert any audio Blob/File to 16kHz PCM WAV for backend compatibility
  const convertToWav16k = async (inputBlobOrFile) => {
    try {
      const arrayBuffer = await inputBlobOrFile.arrayBuffer();
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const decoded = await audioCtx.decodeAudioData(arrayBuffer);

      const targetSampleRate = 16000;
      const offlineCtx = new OfflineAudioContext(1, Math.ceil(decoded.duration * targetSampleRate), targetSampleRate);
      // Mixdown to mono
      const source = offlineCtx.createBufferSource();
      const monoBuffer = offlineCtx.createBuffer(1, decoded.length, decoded.sampleRate);
      const channelData = monoBuffer.getChannelData(0);
      const tmp = new Float32Array(decoded.length);
      for (let ch = 0; ch < decoded.numberOfChannels; ch++) {
        decoded.copyFromChannel(tmp, ch);
        for (let i = 0; i < tmp.length; i++) channelData[i] += tmp[i] / decoded.numberOfChannels;
      }
      source.buffer = monoBuffer;
      source.connect(offlineCtx.destination);
      source.start(0);
      const rendered = await offlineCtx.startRendering();
      const pcm = rendered.getChannelData(0);

      // Float32 -> PCM16 WAV
      const wavBuffer = floatToWav(pcm, targetSampleRate);
      return new File([wavBuffer], 'audio.wav', { type: 'audio/wav' });
    } catch (e) {
      console.error('Audio conversion failed, sending original file:', e);
      // Fallback to original
      if (inputBlobOrFile instanceof File) return inputBlobOrFile;
      return new File([inputBlobOrFile], 'audio.webm', { type: inputBlobOrFile.type || 'audio/webm' });
    }
  };

  const floatToWav = (float32Array, sampleRate) => {
    const numFrames = float32Array.length;
    const buffer = new ArrayBuffer(44 + numFrames * 2);
    const view = new DataView(buffer);
    // RIFF header
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + numFrames * 2, true);
    writeString(view, 8, 'WAVE');
    // fmt chunk
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true); // PCM
    view.setUint16(20, 1, true); // linear PCM
    view.setUint16(22, 1, true); // mono
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true); // byte rate
    view.setUint16(32, 2, true); // block align
    view.setUint16(34, 16, true); // bits per sample
    // data chunk
    writeString(view, 36, 'data');
    view.setUint32(40, numFrames * 2, true);
    // PCM samples
    let offset = 44;
    for (let i = 0; i < numFrames; i++, offset += 2) {
      let s = Math.max(-1, Math.min(1, float32Array[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
    }
    return buffer;
  };

  const writeString = (view, offset, string) => {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };

  // Combined analysis removed per requirements

  const handleTextAnalysis = async (text, contentType, numRecommendations) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('/analyze/text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text,
          content_type: contentType,
          num_recommendations: numRecommendations
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
      console.error('Text analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAudioAnalysis = async (audioFile, contentType, numRecommendations) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const wavFile = await convertToWav16k(audioFile);
      const formData = new FormData();
      formData.append('audio_file', wavFile, wavFile.name);
      formData.append('content_type', contentType);
      formData.append('num_recommendations', numRecommendations);

      const response = await fetch('/analyze/audio', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
      console.error('Audio analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleImageAnalysis = async (imageFile, contentType, numRecommendations) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('image_file', imageFile);
      formData.append('content_type', contentType);
      formData.append('num_recommendations', numRecommendations);

      const response = await fetch('/analyze/image', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
      console.error('Image analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Header activeTab={activeTab} onChangeTab={setActiveTab} />
      
      <main className="main-content">
        <div className="container">
          <div className="hero-section">
            <div className="hero-content">
              <h1 className="hero-title">
                <span className="emoji">🎬</span>
                AI-Powered Movie Recommendations
              </h1>
              <p className="hero-subtitle">
                Discover your perfect movie or TV show based on your emotions using cutting-edge AI analysis
              </p>
              <div className="hero-features">
                <div className="feature">
                  <span className="feature-icon">📝</span>
                  <span>Text Analysis</span>
                </div>
                <div className="feature">
                  <span className="feature-icon">📸</span>
                  <span>Face Analysis</span>
                </div>
                <div className="feature">
                  <span className="feature-icon">🤖</span>
                  <span>AI Powered</span>
                </div>
              </div>
            </div>
          </div>

          <div className="tabs-container">
            <div className="tabs">
              <button 
                className={`tab ${activeTab === 'text' ? 'active' : ''}`}
                onClick={() => setActiveTab('text')}
              >
                <span className="tab-icon">📝</span>
                Text Analysis
              </button>
              <button 
                className={`tab ${activeTab === 'image' ? 'active' : ''}`}
                onClick={() => setActiveTab('image')}
              >
                <span className="tab-icon">📸</span>
                Face Analysis
              </button>
              <button 
                className={`tab ${activeTab === 'combined' ? 'active' : ''}`}
                onClick={() => setActiveTab('combined')}
              >
                <span className="tab-icon">🔗</span>
                Combined
              </button>
            </div>
          </div>

          <InputSection 
            activeTab={activeTab}
            onTextAnalysis={handleTextAnalysis}
            onImageAnalysis={handleImageAnalysis}
            loading={loading}
          />

          {loading && <LoadingSpinner />}

          {error && (
            <div className="error-message">
              <div className="error-icon">⚠️</div>
              <div className="error-content">
                <h3>Oops! Something went wrong</h3>
                <p>{error}</p>
              </div>
            </div>
          )}

          {results && <ResultsSection results={results} />}
        </div>
      </main>

      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2024 OTT Recommendation System. Powered by Hugging Face AI Models.</p>
          <div className="footer-links">
            <a href="#about">About</a>
            <a href="#privacy">Privacy</a>
            <a href="#contact">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;

