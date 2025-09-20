from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
import tempfile
import shutil
from typing import Optional, List
import pandas as pd
import json

# Import our Hugging Face based modules
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from services.unified_recommender_hf import UnifiedOTTRecommender
import warnings
warnings.filterwarnings('ignore')

# Initialize FastAPI app
app = FastAPI(
    title="OTT Recommendation System API",
    description="API for emotion-based movie and TV show recommendations using Hugging Face models",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store the recommender instance
recommender = None

# Pydantic models for request/response
class TextRequest(BaseModel):
    text: str
    content_type: str = "movie"
    num_recommendations: int = 10

class RecommendationResponse(BaseModel):
    emotion_analysis: dict
    recommendations: List[dict]
    content_type: str
    num_recommendations: int

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

# Initialize the recommender system
@app.on_event("startup")
async def startup_event():
    """Initialize the recommender system on startup"""
    global recommender
    try:
        print("🚀 Initializing OTT Recommendation System...")
        recommender = UnifiedOTTRecommender()
        print("✅ System initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        raise e

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OTT Recommendation System API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "system_initialized": recommender is not None
    }

@app.post("/analyze/text", response_model=RecommendationResponse)
async def analyze_text_emotion(request: TextRequest):
    """Analyze text emotion and get recommendations"""
    try:
        if not recommender:
            raise HTTPException(status_code=500, detail="System not initialized")
        
        # Get recommendations
        results = recommender.get_complete_recommendation(
            text=request.text,
            content_type=request.content_type,
            num_recommendations=request.num_recommendations
        )
        
        if 'error' in results:
            raise HTTPException(status_code=400, detail=results['error'])
        
        # Convert recommendations to list of dicts
        recommendations_list = []
        if not results['recommendations'].empty:
            recommendations_list = results['recommendations'].to_dict('records')
        
        return RecommendationResponse(
            emotion_analysis=results['emotion_analysis'],
            recommendations=recommendations_list,
            content_type=results['content_type'],
            num_recommendations=results['num_recommendations']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Audio route removed per requirements

@app.post("/analyze/image", response_model=RecommendationResponse)
async def analyze_image_emotion(
    image_file: UploadFile = File(...),
    content_type: str = Form("movie"),
    num_recommendations: int = Form(10)
):
    """Analyze image emotion and get recommendations"""
    try:
        if not recommender:
            raise HTTPException(status_code=500, detail="System not initialized")
        
        # Validate file type
        if not image_file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image file")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            shutil.copyfileobj(image_file.file, tmp_file)
            tmp_file_path = tmp_file.name
        
        try:
            # Get recommendations
            results = recommender.get_complete_recommendation(
                image_path=tmp_file_path,
                content_type=content_type,
                num_recommendations=num_recommendations
            )
            
            if 'error' in results:
                raise HTTPException(status_code=400, detail=results['error'])
            
            # Convert recommendations to list of dicts
            recommendations_list = []
            if not results['recommendations'].empty:
                recommendations_list = results['recommendations'].to_dict('records')
            
            return RecommendationResponse(
                emotion_analysis=results['emotion_analysis'],
                recommendations=recommendations_list,
                content_type=results['content_type'],
                num_recommendations=results['num_recommendations']
            )
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Combined route removed per requirements

@app.get("/emotions")
async def get_emotions():
    """Get list of supported emotions"""
    return {
        "emotions": [
            {"id": 0, "name": "Sad", "description": "Sadness, depression, loneliness"},
            {"id": 1, "name": "Happy", "description": "Joy, excitement, happiness"},
            {"id": 2, "name": "Surprise", "description": "Surprise, amazement, shock"},
            {"id": 3, "name": "Angry", "description": "Anger, frustration, rage"},
            {"id": 4, "name": "Fear", "description": "Fear, anxiety, worry"},
            {"id": 5, "name": "Disgust", "description": "Disgust, repulsion, aversion"},
            {"id": 6, "name": "Neutral", "description": "Calm, neutral, balanced"}
        ]
    }

@app.get("/content-types")
async def get_content_types():
    """Get list of supported content types"""
    return {
        "content_types": [
            {"id": "movie", "name": "Movies"},
            {"id": "tv_series", "name": "TV Series"}
        ]
    }

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        if not recommender:
            return {"error": "System not initialized"}
        
        # Get movie count from the recommender
        movie_count = len(recommender.movie_recommender.movies_df) if recommender.movie_recommender.movies_df is not None else 0
        
        return {
            "total_movies": movie_count,
            "supported_emotions": 7,
            "supported_content_types": 2,
            "system_status": "operational"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

