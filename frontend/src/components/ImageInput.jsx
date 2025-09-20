import React, { useState, useRef } from 'react';
import '../styles/ImageInput.css';

const ImageInput = ({ onAnalysis, loading }) => {
  const [imageFile, setImageFile] = useState(null);
  const [contentType, setContentType] = useState('movie');
  const [numRecommendations, setNumRecommendations] = useState(10);
  const [capturedImage, setCapturedImage] = useState(null);
  const [isCapturing, setIsCapturing] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImageFile(file);
      setCapturedImage(null);
    } else {
      alert('Please select a valid image file');
    }
  };

  const startCamera = async () => {
    try {
      // Immediately show camera UI
      setIsCapturing(true);
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: 640, 
          height: 480,
          facingMode: 'user'
        } 
      });
      videoRef.current.srcObject = stream;
      // Ensure the video actually starts
      // Some browsers require muted for autoplay
      if (videoRef.current) {
        videoRef.current.muted = true;
      }
      videoRef.current.onloadedmetadata = () => {
        if (videoRef.current) {
          videoRef.current.play().catch(() => {});
        }
      };
    } catch (error) {
      console.error('Error accessing camera:', error);
      alert('Error accessing camera. Please check permissions.');
      setIsCapturing(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setIsCapturing(false);
  };

  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    if (canvas && video) {
      const context = canvas.getContext('2d');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0);
      
      canvas.toBlob((blob) => {
        setCapturedImage(blob);
        stopCamera();
      }, 'image/jpeg', 0.8);
    }
  };

  const captureAndAnalyze = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (canvas && video) {
      const context = canvas.getContext('2d');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0);
      canvas.toBlob((blob) => {
        setCapturedImage(blob);
        stopCamera();
        onAnalysis(blob, contentType, numRecommendations);
      }, 'image/jpeg', 0.9);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const imageToAnalyze = capturedImage || imageFile;
    if (imageToAnalyze) {
      onAnalysis(imageToAnalyze, contentType, numRecommendations);
    }
  };

  const clearImage = () => {
    setImageFile(null);
    setCapturedImage(null);
    stopCamera();
  };

  return (
    <div className="image-input">
      <div className="input-header">
        <h3>📸 Image Emotion Analysis</h3>
        <p>Upload a photo or take a selfie to analyze facial expressions</p>
      </div>

      <form onSubmit={handleSubmit} className="image-form">
        <div className="image-options">
          <div className="image-option">
            <h4>📁 Upload Image</h4>
            <div className="file-upload">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="file-input"
                id="image-file"
                disabled={loading || isCapturing}
              />
              <label htmlFor="image-file" className="file-label">
                Choose Image File
              </label>
              {imageFile && (
                <div className="file-info">
                  <img 
                    src={URL.createObjectURL(imageFile)} 
                    alt="Preview" 
                    className="image-preview"
                  />
                  <span>📄 {imageFile.name}</span>
                  <button type="button" onClick={clearImage} className="clear-btn">
                    ✕
                  </button>
                  <button
                    type="button"
                    className="analyze-inline-btn"
                    onClick={() => onAnalysis(imageFile, contentType, numRecommendations)}
                    disabled={loading}
                  >
                    Analyze this image
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="divider">OR</div>

          <div className="image-option">
            <h4>📷 Take Photo</h4>
            <div className="camera-controls">
              {!isCapturing ? (
                <button
                  type="button"
                  onClick={startCamera}
                  className="camera-btn"
                  disabled={loading}
                >
                  📷 Start Camera
                </button>
              ) : (
                <div className="camera-interface">
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="camera-video"
                  />
                  <button
                    type="button"
                    onClick={captureImage}
                    className="capture-btn"
                  >
                    📸 Capture
                  </button>
                  <button
                    type="button"
                    onClick={captureAndAnalyze}
                    className="capture-btn"
                  >
                    🚀 Capture & Analyze
                  </button>
                  <button
                    type="button"
                    onClick={stopCamera}
                    className="cancel-btn"
                  >
                    ❌ Cancel
                  </button>
                </div>
              )}
              
              {capturedImage && (
                <div className="captured-image">
                  <img 
                    src={URL.createObjectURL(capturedImage)} 
                    alt="Captured" 
                    className="image-preview"
                  />
                  <span>📸 Photo captured</span>
                  <button type="button" onClick={clearImage} className="clear-btn">
                    ✕ Clear
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        <canvas ref={canvasRef} style={{ display: 'none' }} />

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="content-type" className="form-label">
              Content Type
            </label>
            <select
              id="content-type"
              value={contentType}
              onChange={(e) => setContentType(e.target.value)}
              className="form-select"
              disabled={loading}
            >
              <option value="movie">Movies</option>
              <option value="tv_series">TV Series</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="num-recommendations" className="form-label">
              Number of Recommendations
            </label>
            <select
              id="num-recommendations"
              value={numRecommendations}
              onChange={(e) => setNumRecommendations(parseInt(e.target.value))}
              className="form-select"
              disabled={loading}
            >
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={15}>15</option>
              <option value={20}>20</option>
            </select>
          </div>
        </div>

        <button 
          type="submit" 
          className="submit-btn"
          disabled={loading || (!imageFile && !capturedImage)}
        >
          {loading ? 'Analyzing Image...' : 'Analyze Emotion & Get Recommendations'}
        </button>
      </form>

      <div className="info-box">
        <h4>ℹ️ Image Analysis Tips:</h4>
        <ul>
          <li>Make sure your face is clearly visible and well-lit</li>
          <li>Supported formats: JPG, PNG, JPEG</li>
          <li>Our AI analyzes facial expressions to detect emotions</li>
          <li>For best results, look directly at the camera</li>
        </ul>
      </div>
    </div>
  );
};

export default ImageInput;








