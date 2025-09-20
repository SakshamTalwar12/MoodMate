TEXT_EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
# Alternatives:
# TEXT_EMOTION_MODEL = "cardiffnlp/twitter-roberta-base-emotion"
# TEXT_EMOTION_MODEL = "michellejieli/emotion_text_classifier"

# Face Emotion Classification Models
FACE_EMOTION_MODEL = "trpakov/vit-face-expression"
# Alternatives:
# FACE_EMOTION_MODEL = "microsoft/DialoGPT-medium"
# FACE_EMOTION_MODEL = "google/vit-base-patch16-224"


# Text Emotion Mapping (maps model output to our system emotions)
TEXT_EMOTION_MAPPING = {
    'joy': 1,          # Happy/Joy
    'sadness': 0,      # Sad
    'anger': 3,        # Angry
    'fear': 4,         # Fear
    'disgust': 5,      # Disgust/Lazy
    'surprise': 2,     # Love/Surprise
    'neutral': 6       # Neutral
}


# Face Emotion Mapping
FACE_EMOTION_MAPPING = {
    'happy': 1,        # Happy
    'sad': 0,          # Sad
    'angry': 3,        # Angry
    'fear': 4,         # Fear
    'disgust': 5,      # Disgust
    'surprise': 2,     # Surprise
    'neutral': 6       # Neutral
}

# Model Settings
MODEL_SETTINGS = {
    'return_all_scores': True,
    'device': 'auto',  # 'auto', 'cpu', 'cuda'
    'batch_size': 1,
    'max_length': 512
}

EMOTION_LABELS = {
    0: 'Sad',
    1: 'Happy/Joy',
    2: 'Love/Surprise',
    3: 'Angry',
    4: 'Fear',
    5: 'Lazy/Disgust',
    6: 'Neutral'
}

CONTENT_TYPES = {
    'movie': 'Movies',
    'tv_series': 'TV Series'
}

RECOMMENDATION_SETTINGS = {
    'default_num_recommendations': 10,
    'max_recommendations': 50,
    'min_recommendations': 1
}

API_SETTINGS = {
    'host': '0.0.0.0',
    'port': 8000,
    'reload': True,
    'log_level': 'info'
}

FRONTEND_SETTINGS = {
    'port': 3000,
    'host': 'localhost'
}
