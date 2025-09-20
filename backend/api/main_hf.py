import os
import sys
import warnings
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from unified_recommender_hf import UnifiedOTTRecommender
import tempfile
import shutil
import uvicorn

warnings.filterwarnings('ignore')

app = FastAPI(title="OTT Recommendation System (HuggingFace Edition)")

# Initialize recommender
recommender = UnifiedOTTRecommender()

class TextInput(BaseModel):
    text: str
    num_recommendations: int = 5

@app.get("/")
def root():
    return {"message": "🎬 Welcome to OTT Recommendation System (Hugging Face Edition)"}

@app.post("/recommend/text")
def recommend_from_text(payload: TextInput):
    try:
        results = recommender.get_complete_recommendation(
            text=payload.text,
            num_recommendations=payload.num_recommendations
        )
        return {"recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommend/text")
def recommend_text_get():
    return {"message": "Use POST with JSON body: {'text': 'your mood', 'num_recommendations': 5}"}

@app.post("/recommend/image")
def recommend_from_image(
    image_file: UploadFile = File(...),
    num_recommendations: int = Form(5)
):
    try:
        if not image_file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Save image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            shutil.copyfileobj(image_file.file, tmp_file)
            tmp_path = tmp_file.name

        try:
            results = recommender.get_complete_recommendation(
                image_path=tmp_path,
                num_recommendations=num_recommendations
            )
            return {"recommendations": results}
        finally:
            os.unlink(tmp_path)  # cleanup
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("CLI mode has been disabled (only text & image supported).")
    else:
        uvicorn.run("main_hf:app", host="127.0.0.1", port=8000, reload=True)
