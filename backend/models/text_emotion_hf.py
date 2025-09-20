import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import warnings
import sys
import os
warnings.filterwarnings('ignore')

# Add config path to import
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from models_config import TEXT_EMOTION_MODEL, TEXT_EMOTION_MAPPING, MODEL_SETTINGS

class TextEmotionClassifier:
    def __init__(self):
        """Initialize the text emotion classifier using Hugging Face models"""
        # Using centralized model configuration
        self.model_name = TEXT_EMOTION_MODEL
        self.classifier = pipeline(
            "text-classification",
            model=self.model_name,
            return_all_scores=MODEL_SETTINGS['return_all_scores']
        )
        
        # Use centralized emotion mapping
        self.emotion_mapping = TEXT_EMOTION_MAPPING
    
    def predict_emotion(self, text):
        """
        Predict emotion from text using Hugging Face model
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            int: Emotion class (0=sad, 1=happy, 2=surprise, 3=angry, 4=fear, 5=disgust)
        """
        try:
            # Get predictions from the model
            results = self.classifier(text)
            
            # Find the emotion with highest confidence
            best_emotion = max(results[0], key=lambda x: x['score'])
            emotion_label = best_emotion['label']
            confidence = best_emotion['score']
            
            # Map to our emotion system
            emotion_class = self.emotion_mapping.get(emotion_label, 0)  # default to sad
            
            return emotion_class, confidence, emotion_label
            
        except Exception as e:
            print(f"Error in emotion prediction: {e}")
            return 0, 0.0, "error"  # default to sad
    
    def get_emotion_probabilities(self, text):
        """
        Get probability distribution for all emotions
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Dictionary with emotion probabilities
        """
        try:
            results = self.classifier(text)
            emotion_probs = {}
            
            for result in results[0]:
                emotion_label = result['label']
                probability = result['score']
                emotion_probs[emotion_label] = probability
            
            return emotion_probs
            
        except Exception as e:
            print(f"Error getting emotion probabilities: {e}")
            return {}

# Example usage
if __name__ == "__main__":
    # Initialize the classifier
    text_classifier = TextEmotionClassifier()
    
    # Test with sample texts
    test_texts = [
        "I am so happy today!",
        "This makes me really angry",
        "I'm scared of the dark",
        "I feel so sad and lonely",
        "What a surprise!",
        "This is disgusting"
    ]
    
    print("Text Emotion Classification Results:")
    print("=" * 50)
    
    for text in test_texts:
        emotion_class, confidence, emotion_label = text_classifier.predict_emotion(text)
        print(f"Text: '{text}'")
        print(f"Predicted Emotion: {emotion_label} (Class: {emotion_class})")
        print(f"Confidence: {confidence:.3f}")
        print("-" * 30)
