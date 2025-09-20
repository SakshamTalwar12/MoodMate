import torch
import cv2
from PIL import Image
import numpy as np
from transformers import pipeline
import warnings
import sys
import os
warnings.filterwarnings('ignore')

# Add config path to import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from models_config import FACE_EMOTION_MODEL, FACE_EMOTION_MAPPING, MODEL_SETTINGS

class FaceEmotionClassifier:
    def __init__(self):
        """Initialize the face emotion classifier using Hugging Face models"""
        # Using centralized model configuration
        self.model_name = FACE_EMOTION_MODEL
        self.classifier = pipeline(
            "image-classification",
            model=self.model_name
        )
        
        # Use centralized emotion mapping
        self.emotion_mapping = FACE_EMOTION_MAPPING
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for emotion classification
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            np.array: Preprocessed image array
        """
        try:
            # Prefer PIL for broader format support (png, webp, etc.)
            try:
                with Image.open(image_path) as img:
                    image = img.convert('RGB')
                    # Return PIL Image directly for pipeline compatibility
                    return image
            except Exception as pil_e:
                print(f"PIL failed to open image ({pil_e}), falling back to OpenCV")
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Could not load image from {image_path}")
                    return None
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                return Image.fromarray(image)
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def preprocess_array(self, image_array):
        """
        Preprocess image array for emotion classification
        
        Args:
            image_array (np.array): Image array (BGR format from OpenCV)
            
        Returns:
            np.array: Preprocessed image array (RGB format)
        """
        try:
            # Convert BGR to RGB if needed
            if len(image_array.shape) == 3 and image_array.shape[2] == 3:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            return Image.fromarray(image_array)
            
        except Exception as e:
            print(f"Error preprocessing image array: {e}")
            return None
    
    def predict_emotion(self, image_path):
        """
        Predict emotion from image using Hugging Face model
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            int: Emotion class (0=sad, 1=happy, 2=surprise, 3=angry, 4=fear, 5=disgust, 6=neutral)
        """
        try:
            # Preprocess image
            image = self.preprocess_image(image_path)
            if image is None:
                return 0, 0.0, "error"
            
            # Get predictions from the model
            results = self.classifier(image)
            # HF pipeline may return List[Dict] or List[List[Dict]] depending on batching
            candidates = results if (len(results) and isinstance(results[0], dict)) else results[0]
            # Find the emotion with highest confidence
            best_emotion = max(candidates, key=lambda x: x.get('score', 0))
            emotion_label = str(best_emotion.get('label', '')).lower()
            # Normalize common label variants
            label_norm = {
                'happiness': 'happy', 'joy': 'happy',
                'sadness': 'sad',
                'anger': 'angry', 'angry': 'angry',
                'fear': 'fear', 'scared': 'fear',
                'disgust': 'disgust',
                'surprise': 'surprise', 'surprised': 'surprise',
                'neutral': 'neutral'
            }
            emotion_label = label_norm.get(emotion_label, emotion_label)
            confidence = float(best_emotion.get('score', 0))
            
            # Map to our emotion system
            emotion_class = self.emotion_mapping.get(emotion_label, 6)  # default to neutral
            
            return emotion_class, confidence, emotion_label
            
        except Exception as e:
            print(f"Error in face emotion prediction: {e}")
            return 0, 0.0, "error"  # default to sad
    
    def predict_emotion_from_array(self, image_array):
        """
        Predict emotion from image array
        
        Args:
            image_array (np.array): Image data array
            
        Returns:
            int: Emotion class
        """
        try:
            # Preprocess image array
            image_array = self.preprocess_array(image_array)
            if image_array is None:
                return 0, 0.0, "error"
            
            # Get predictions from the model
            results = self.classifier(image_array)
            candidates = results if (len(results) and isinstance(results[0], dict)) else results[0]
            # Find the emotion with highest confidence
            best_emotion = max(candidates, key=lambda x: x.get('score', 0))
            emotion_label = str(best_emotion.get('label', '')).lower()
            label_norm = {
                'happiness': 'happy', 'joy': 'happy',
                'sadness': 'sad',
                'anger': 'angry', 'angry': 'angry',
                'fear': 'fear', 'scared': 'fear',
                'disgust': 'disgust',
                'surprise': 'surprise', 'surprised': 'surprise',
                'neutral': 'neutral'
            }
            emotion_label = label_norm.get(emotion_label, emotion_label)
            confidence = float(best_emotion.get('score', 0))
            
            # Map to our emotion system
            emotion_class = self.emotion_mapping.get(emotion_label, 6)
            
            return emotion_class, confidence, emotion_label
            
        except Exception as e:
            print(f"Error in face emotion prediction: {e}")
            return 0, 0.0, "error"
    
    def get_emotion_probabilities(self, image_path):
        """
        Get probability distribution for all emotions
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            dict: Dictionary with emotion probabilities
        """
        try:
            # Preprocess image
            image = self.preprocess_image(image_path)
            if image is None:
                return {}
            
            results = self.classifier(image)
            emotion_probs = {}
            
            for result in results[0]:
                emotion_label = result['label']
                probability = result['score']
                emotion_probs[emotion_label] = probability
            
            return emotion_probs
            
        except Exception as e:
            print(f"Error getting emotion probabilities: {e}")
            return {}
    
    def detect_face_and_predict(self, image_path):
        """
        Detect face in image and predict emotion
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            tuple: (emotion_class, confidence, emotion_label, face_detected)
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return 0, 0.0, "error", False
            
            # Load face cascade classifier
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                print("No face detected in the image")
                return 0, 0.0, "no_face", False
            
            # Use the first detected face
            x, y, w, h = faces[0]
            face_roi = image[y:y+h, x:x+w]
            
            # Predict emotion from face region
            emotion_class, confidence, emotion_label = self.predict_emotion_from_array(face_roi)
            
            return emotion_class, confidence, emotion_label, True
            
        except Exception as e:
            print(f"Error in face detection and emotion prediction: {e}")
            return 0, 0.0, "error", False

# Example usage
if __name__ == "__main__":
    # Initialize the classifier
    face_classifier = FaceEmotionClassifier()
    
    # Test with sample image file (you would need to provide an actual image file)
    # image_path = "sample_face.jpg"
    # emotion_class, confidence, emotion_label, face_detected = face_classifier.detect_face_and_predict(image_path)
    # if face_detected:
    #     print(f"Predicted Emotion: {emotion_label} (Class: {emotion_class})")
    #     print(f"Confidence: {confidence:.3f}")
    # else:
    #     print("No face detected or error occurred")
    
    print("Face Emotion Classifier initialized successfully!")
    print("Use detect_face_and_predict(image_path) to classify emotions from face images.")
