import pandas as pd
import numpy as np
import warnings
import sys
import os
warnings.filterwarnings('ignore')

# Add the parent directory to path to import from other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing modules with correct paths
try:
    # Import from models directory
    from models.text_emotion_hf import TextEmotionClassifier
    from models.face_emotion_hf import FaceEmotionClassifier
    # Import from same services directory
    from services.movie_recommender_hf import MovieRecommenderHF
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required modules are available")
    raise

class UnifiedOTTRecommender:
    def __init__(self):
        """Initialize the unified OTT recommendation system"""
        print("Initializing Unified OTT Recommendation System...")
        
        # Initialize emotion classifier
        try:
            self.text_classifier = TextEmotionClassifier()
            print("✅ Text emotion classifier initialized")
        except Exception as e:
            print(f"❌ Error initializing text classifier: {e}")
            self.text_classifier = None
        
        # Initialize face emotion classifier
        try:
            self.face_classifier = FaceEmotionClassifier()
            print("✅ Face emotion classifier initialized")
        except Exception as e:
            print(f"❌ Error initializing face classifier: {e}")
            self.face_classifier = None
        
        # Initialize movie recommender
        try:
            self.movie_recommender = MovieRecommenderHF()
            print("✅ Movie recommender initialized")
        except Exception as e:
            print(f"❌ Error initializing movie recommender: {e}")
            self.movie_recommender = None
        
        # Emotion labels mapping
        self.emotion_labels = {
            0: 'Sad',
            1: 'Happy',
            2: 'Surprise', 
            3: 'Angry',
            4: 'Fear',
            5: 'Disgust',
            6: 'Neutral'
        }
        
        print("✅ System initialized successfully!")
    
    def analyze_text_emotion(self, text):
        """Analyze emotion from text input"""
        try:
            if not self.text_classifier:
                print("❌ Text classifier not available")
                return None
            
            emotion_class, confidence, emotion_label = self.text_classifier.predict_emotion(text)
            
            return {
                'emotion_class': emotion_class,
                'emotion_label': self.emotion_labels.get(emotion_class, emotion_label),
                'confidence': confidence,
                'method': 'text'
            }
        except Exception as e:
            print(f"Error in text emotion analysis: {e}")
            return None
    
    def get_complete_recommendation(self, 
                                  text=None,
                                  audio_path=None,
                                  image_path=None,
                                  content_type="movie",
                                  num_recommendations=10):
        """
        Get complete recommendations based on multiple input types
        """
        try:
            emotion_analysis = None
            
            # Process text input
            if text:
                emotion_analysis = self.analyze_text_emotion(text)
                print(f"📝 Text emotion analysis: {emotion_analysis}")
            
            # Image analysis
            if image_path and not emotion_analysis and self.face_classifier:
                try:
                    # First try face detection path
                    emotion_class, confidence, raw_label, face_detected = self.face_classifier.detect_face_and_predict(image_path)
                    if face_detected:
                        emotion_analysis = {
                            'emotion_class': emotion_class,
                            'emotion_label': self.emotion_labels.get(emotion_class, raw_label),
                            'confidence': float(confidence),
                            'method': 'image'
                        }
                        print(f"📸 Image emotion analysis (face): {emotion_analysis}")
                    else:
                        # Fallback: classify whole image
                        emotion_class, confidence, raw_label = self.face_classifier.predict_emotion(image_path)
                        emotion_analysis = {
                            'emotion_class': emotion_class,
                            'emotion_label': self.emotion_labels.get(emotion_class, raw_label),
                            'confidence': float(confidence),
                            'method': 'image'
                        }
                        print(f"📸 Image emotion analysis (full-image): {emotion_analysis}")
                except Exception as e:
                    print(f"❌ Image analysis failed: {e}")
            
            # Image analysis not implemented in this HF variant
            
            if not emotion_analysis:
                return {'error': 'No input provided or emotion analysis failed'}
            
            # Get recommendations
            if not self.movie_recommender:
                return {'error': 'Movie recommender not initialized'}
            
            print(f"🎬 Getting recommendations for emotion: {emotion_analysis['emotion_label']}")
            recommendations = self.movie_recommender.recommend_movies(
                emotion_analysis['emotion_class'],
                num_recommendations,
                content_type
            )
            
            print(f"✅ Found {len(recommendations)} recommendations")
            
            return {
                'emotion_analysis': emotion_analysis,
                'recommendations': recommendations,
                'content_type': content_type,
                'num_recommendations': num_recommendations
            }
            
        except Exception as e:
            print(f"❌ Error in complete recommendation: {e}")
            import traceback
            traceback.print_exc()
            return {
                'error': str(e),
                'recommendations': pd.DataFrame()
            }
    
    def display_recommendations(self, results):
        """Display recommendation results in a formatted way"""
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            return
        
        emotion_analysis = results['emotion_analysis']
        recommendations = results['recommendations']
        
        print("\n" + "="*60)
        print("🎬 OTT RECOMMENDATION SYSTEM - RESULTS")
        print("="*60)
        
        # Display emotion analysis
        print(f"\n🎭 Emotion Analysis:")
        print(f"   Detected Emotion: {emotion_analysis['emotion_label']}")
        print(f"   Confidence: {emotion_analysis['confidence']:.2f}")
        print(f"   Method: {emotion_analysis['method']}")
        
        # Display recommendations
        print(f"\n🎬 Recommendations ({results['content_type'].upper()}):")
        print("-" * 40)
        
        if recommendations.empty:
            print("   No recommendations available")
        else:
            for idx, movie in recommendations.iterrows():
                print(f"\n{idx+1}. {movie['title']} ({movie.get('year', 'N/A')})")
                if 'rating' in movie:
                    print(f"   ⭐ Rating: {movie['rating']:.1f}")
                if 'genres' in movie:
                    genres = movie['genres'] if isinstance(movie['genres'], str) else ', '.join(movie['genres'])
                    print(f"   🎭 Genres: {genres}")
                if 'overview' in movie:
                    print(f"   📝 Overview: {movie['overview'][:150]}...")
        
        print("\n" + "="*60)

# Test the system if run directly
if __name__ == "__main__":
    print("🧪 Testing Unified OTT Recommender...")
    
    try:
        # Initialize the system
        recommender = UnifiedOTTRecommender()
        
        # Test with a simple text input
        test_text = "I'm feeling really happy today!"
        results = recommender.get_complete_recommendation(
            text=test_text, 
            num_recommendations=3
        )
        
        recommender.display_recommendations(results)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()