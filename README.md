<h1>🎬 Mood-Mate</h1>

<p>
A modern full-stack recommendation system that detects user emotions (via text or facial expressions) using Hugging Face models and provides 
<strong>personalized movie/TV show recommendations</strong> based on mood.
</p>

<h2>🏗️ Architecture</h2>

<p>OTT Recommendation Tool is built with a modern three-tier architecture:</p>
<ul>
  <li><strong>Frontend:</strong> React.js with Vanilla CSS</li>
  <li><strong>Backend API:</strong> FastAPI with Python, Hugging Face Transformers, PyTorch, OpenCV, Pillow, Uvicorn</li>
  <li><strong>Database / Storage:</strong> (Optional) PostgreSQL or local storage for user preferences & caching <em>(not included in this version)</em></li>
</ul>

<h2>🚀 Features</h2>

<h3>Core Features</h3>
<ul>
  <li><strong>Text Emotion Analysis:</strong> Detects emotions using <code>j-hartmann/emotion-english-distilroberta-base</code></li>
  <li><strong>Face Emotion Analysis:</strong> Facial expression recognition using <code>trpakov/vit-face-expression</code></li>
  <li><strong>Movie Database:</strong> 28,655+ movies from Hugging Face <code>mt0rm0/movie_descriptors_small</code> dataset</li>
  <li><strong>Unified Recommendation Engine:</strong> Combines multiple detection methods for higher accuracy</li>
  <li><strong>Real-Time Recommendations:</strong> Instant suggestions tailored to detected emotions</li>
</ul>

<h3>AI Features</h3>
<ul>
  <li><strong>Emotion-to-Genre Mapping:</strong> Maps mood to preferred movie genres</li>
  <li><strong>Rating-Based Filtering:</strong> Only movies with ≥ 7.0 rating are recommended</li>
  <li><strong>Recency Preference:</strong> Gives slight priority to recent releases</li>
  <li><strong>Fast Inference:</strong> ~1–3 seconds per request</li>
</ul>

<h2>📁 Project Structure</h2>

<pre>
ott-recommendation-tool/
├── frontend/                 # React.js frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Main application pages
│   │   ├── styles/          # CSS stylesheets
│   │   └── App.js           # Main entry point
│   └── package.json         # Frontend dependencies
│
├── backend/                  # FastAPI backend
│   ├── api/                  # API routes
│   ├── models/               # Model loading & management
│   ├── services/             # Business logic for recommendations
│   ├── app.py                # FastAPI entry point
│   └── requirements_hf.txt   # Python dependencies
│
└── README.md                 # Documentation
</pre>

<h2>🛠️ Technology Stack</h2>

<h3>Frontend</h3>
<ul>
  <li><strong>React.js 19:</strong> Modern React with functional components</li>
  <li><strong>CSS3:</strong> Responsive styling with flexbox/grid</li>
  <li><strong>Axios / Fetch API:</strong> Communication with backend</li>
</ul>

<h3>Backend API</h3>
<ul>
  <li><strong>FastAPI:</strong> High-performance Python web framework</li>
  <li><strong>Hugging Face Transformers:</strong> Pre-trained NLP & vision models</li>
  <li><strong>PyTorch:</strong> Deep learning framework</li>
  <li><strong>OpenCV + Pillow:</strong> Image preprocessing & facial detection</li>
  <li><strong>Uvicorn:</strong> ASGI server for async requests</li>
</ul>

<h3>Database / Storage (Optional)</h3>
<ul>
  <li><strong>PostgreSQL:</strong> Persistent storage for preferences/history <em>(not included)</em></li>
  <li><strong>Local Caching:</strong> Hugging Face datasets & models cached for speed</li>
</ul>

<h2>📋 Prerequisites</h2>
<ul>
  <li><strong>Node.js</strong> (v16 or higher)</li>
  <li><strong>Python</strong> (v3.8 or higher)</li>
  <li><strong>Git</strong> (for cloning the repo)</li>
  <li><em>(Optional)</em> <strong>PostgreSQL</strong> for persistent storage</li>
</ul>

<h2>🔧 Installation & Setup</h2>

<h3>1. Clone the Repository</h3>
<pre>
git clone https://github.com/SakshamTalwar12/OTT-Recommendation-Tool.git
cd OTT-Recommendation-Tool
</pre>

<h3>2. Install Backend Dependencies</h3>
<pre>
cd backend
pip install -r requirements_hf.txt
</pre>

<h3>3. Start the Backend Server</h3>
<pre>
uvicorn app:app --reload
</pre>
<p>Backend will run at <code>http://127.0.0.1:8000</code></p>

<h3>4. Install Frontend Dependencies</h3>
<pre>
cd ../frontend
npm install
</pre>

<h3>5. Start the Frontend</h3>
<pre>
npm start
</pre>
<p>Frontend will run at <code>http://localhost:3000</code></p>

<h2>⚡ Usage</h2>
<ul>
  <li>Open the web app at <code>http://localhost:3000</code></li>
  <li>Choose <strong>Text Input</strong> or <strong>Face Emotion Detection</strong></li>
  <li>Submit input & receive instant movie/TV recommendations</li>
</ul>

<h2>🔮 Future Improvements</h2>
<ul>
  <li>🎥 Add trailers and OTT platform links</li>
  <li>⭐ Personalized recommendations based on user history</li>
  <li>📊 Analytics dashboard for emotion trends</li>
  <li>📱 Deploy mobile-friendly UI</li>
</ul>

<h2>🤝 Contributing</h2>
<p>
Contributions are welcome! Please fork the repo and submit a pull request.
</p>

<h2>📜 License</h2>
<p>
This project is licensed under the <strong>MIT License</strong>.
</p>
