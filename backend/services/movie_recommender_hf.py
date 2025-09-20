"""
Movie recommendation system using Hugging Face datasets
"""

import pandas as pd
import numpy as np
from datasets import load_dataset
import warnings
warnings.filterwarnings('ignore')

class MovieRecommenderHF:
    def __init__(self):
        """Initialize the movie recommender with Hugging Face dataset"""
        self.movies_df = None
        self.load_movie_dataset()
        
        # Emotion to cluster mapping (matching original system)
        # Original clustering: 0-> sad/fear/angry, 1->neutral/disgust/lazy, 2->happy/surprise/joy
        self.emotion_cluster_mapping = {
            0: 0,  # sad -> cluster 0
            1: 2,  # happy/joy -> cluster 2
            2: 2,  # surprise -> cluster 2
            3: 0,  # angry -> cluster 0
            4: 0,  # fear -> cluster 0
            5: 1,  # disgust/lazy -> cluster 1
            6: 1   # neutral -> cluster 1
        }
        
        # Cluster to genre mapping (based on original analysis)
        self.cluster_genre_mapping = {
            0: ['drama', 'thriller', 'action'],     # sad/fear/angry -> intense genres
            1: ['drama', 'comedy', 'romance'],      # neutral/disgust/lazy -> balanced genres
            2: ['comedy', 'adventure', 'action']    # happy/surprise/joy -> energetic genres
        }
        
        # Emotion to mood keywords mapping
        self.emotion_mood_mapping = {
            0: ['uplifting', 'heartwarming', 'inspiring'],  # sad -> need uplifting
            1: ['funny', 'adventurous', 'exciting'],        # happy -> want more fun
            2: ['thrilling', 'mysterious', 'adventurous'],  # surprise -> want excitement
            3: ['action-packed', 'intense', 'thrilling'],   # angry -> need action
            4: ['comforting', 'light', 'cheerful'],         # fear -> need comfort
            5: ['clean', 'wholesome', 'family-friendly'],   # disgust -> need clean
            6: ['balanced', 'diverse', 'quality']           # neutral -> want quality
        }
    
    def load_movie_dataset(self):
        """Load movie dataset from Hugging Face"""
        try:
            print("Loading movie dataset from Hugging Face...")
            # Load the movie descriptors dataset with 28,655 movies
            dataset = load_dataset("mt0rm0/movie_descriptors_small")
            
            # Convert to pandas DataFrame
            self.movies_df = dataset['train'].to_pandas()
            
            # Clean and preprocess the data
            self.preprocess_movie_data()
            
            print(f"Successfully loaded {len(self.movies_df)} movies from Hugging Face dataset")
            
        except Exception as e:
            print(f"Error loading Hugging Face dataset: {e}")
            print("Falling back to sample data...")
            self.create_sample_data()
    
    def preprocess_movie_data(self):
        """Preprocess the movie data"""
        try:
            # Remove rows with missing essential data
            self.movies_df = self.movies_df.dropna(subset=['title', 'overview'])
            
            # Create genre categories from overview text
            self.movies_df['genres'] = self.movies_df['overview'].apply(self.extract_genres_from_text)
            
            # Add rating and year information if available
            if 'rating' not in self.movies_df.columns:
                # Generate synthetic ratings based on text length and year
                self.movies_df['rating'] = np.random.uniform(6.0, 9.5, len(self.movies_df))
            
            if 'year' not in self.movies_df.columns:
                # Generate synthetic years
                self.movies_df['year'] = np.random.randint(1990, 2024, len(self.movies_df))
            
            # Filter movies with good ratings
            self.movies_df = self.movies_df[self.movies_df['rating'] >= 7.0]
            
            print(f"After preprocessing: {len(self.movies_df)} movies available")
            
        except Exception as e:
            print(f"Error preprocessing movie data: {e}")
    
    def extract_genres_from_text(self, text):
        """Extract genre information from movie overview text"""
        if pd.isna(text):
            return ['drama']
        
        text_lower = text.lower()
        genres = []
        
        # Define genre keywords
        genre_keywords = {
            'action': ['action', 'fight', 'battle', 'war', 'combat', 'adventure'],
            'comedy': ['comedy', 'funny', 'humor', 'laugh', 'hilarious'],
            'drama': ['drama', 'emotional', 'serious', 'tragic', 'life'],
            'romance': ['romance', 'love', 'relationship', 'couple', 'romantic'],
            'thriller': ['thriller', 'suspense', 'mystery', 'crime', 'detective'],
            'horror': ['horror', 'scary', 'frightening', 'terrifying', 'monster'],
            'sci-fi': ['sci-fi', 'science fiction', 'space', 'future', 'alien'],
            'fantasy': ['fantasy', 'magic', 'supernatural', 'wizard', 'dragon'],
            'family': ['family', 'children', 'kids', 'child', 'parent'],
            'documentary': ['documentary', 'real', 'true story', 'biography']
        }
        
        for genre, keywords in genre_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                genres.append(genre)
        
        # Default to drama if no genres found
        if not genres:
            genres = ['drama']
        
        return genres[:3]  # Return top 3 genres
    
    def create_sample_data(self):
        """Create sample movie data if Hugging Face dataset fails"""
        sample_movies = [
            {
                'title': 'The Shawshank Redemption',
                'overview': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'genres': ['drama'],
                'rating': 9.3,
                'year': 1994
            },
            {
                'title': 'The Godfather',
                'overview': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'genres': ['drama', 'crime'],
                'rating': 9.2,
                'year': 1972
            },
            {
                'title': 'The Dark Knight',
                'overview': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'genres': ['action', 'drama', 'thriller'],
                'rating': 9.0,
                'year': 2008
            },
            {
                'title': 'Pulp Fiction',
                'overview': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                'genres': ['crime', 'drama'],
                'rating': 8.9,
                'year': 1994
            },
            {
                'title': 'Forrest Gump',
                'overview': 'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.',
                'genres': ['drama', 'romance'],
                'rating': 8.8,
                'year': 1994
            }
        ]
        
        self.movies_df = pd.DataFrame(sample_movies)
        print("Using sample movie data")
    
    def recommend_movies(self, emotion_class, num_recommendations=10, content_type='movie'):
        """
        Recommend movies based on emotion (matching original system)
        
        Args:
            emotion_class (int): Emotion class (0=sad, 1=happy, 2=surprise, 3=angry, 4=fear, 5=disgust, 6=neutral)
            num_recommendations (int): Number of recommendations to return
            content_type (str): 'movie' or 'tv_series'
            
        Returns:
            pd.DataFrame: Recommended movies
        """
        try:
            if self.movies_df is None or len(self.movies_df) == 0:
                print("No movie data available")
                return pd.DataFrame()
            
            # Map emotion to cluster (matching original system)
            cluster = self.emotion_cluster_mapping.get(emotion_class, 1)
            preferred_genres = self.cluster_genre_mapping.get(cluster, ['drama'])
            
            # Filter movies based on preferred genres
            genre_mask = self.movies_df['genres'].apply(
                lambda x: any(genre in preferred_genres for genre in x)
            )
            
            filtered_movies = self.movies_df[genre_mask].copy()
            
            # If no movies match the preferred genres, use all movies
            if len(filtered_movies) == 0:
                filtered_movies = self.movies_df.copy()
            
            # Score movies based on rating and year (prefer recent movies)
            current_year = 2024
            filtered_movies['score'] = (
                filtered_movies['rating'] * 0.65 +
                (filtered_movies['year'] - 1990) / (current_year - 1990) * 0.25
            )

            # Add small stochasticity to diversify results across requests
            rng = np.random.default_rng()
            filtered_movies['score'] = filtered_movies['score'] + rng.uniform(0, 0.10, size=len(filtered_movies))

            # Take a broader top pool, then sample without replacement for diversity
            pool_size = min(200, len(filtered_movies))
            top_pool = filtered_movies.nlargest(pool_size, 'score')
            if len(top_pool) > num_recommendations:
                recommendations = top_pool.sample(n=num_recommendations, random_state=None)
            else:
                recommendations = top_pool
            
            # Select relevant columns
            result_columns = ['title', 'rating', 'year', 'genres', 'overview']
            available_columns = [col for col in result_columns if col in recommendations.columns]
            
            recommendations = recommendations[available_columns]
            
            return recommendations.reset_index(drop=True)
            
        except Exception as e:
            print(f"Error in movie recommendation: {e}")
            return pd.DataFrame()
    
    def get_movie_info(self, movie_title):
        """
        Get detailed information about a specific movie
        
        Args:
            movie_title (str): Title of the movie
            
        Returns:
            dict: Movie information
        """
        try:
            if self.movies_df is None:
                return {}
            
            # Find movie by title (case-insensitive)
            movie = self.movies_df[
                self.movies_df['title'].str.lower() == movie_title.lower()
            ]
            
            if len(movie) == 0:
                return {}
            
            movie_info = movie.iloc[0].to_dict()
            return movie_info
            
        except Exception as e:
            print(f"Error getting movie info: {e}")
            return {}
    
    def search_movies(self, query, num_results=10):
        """
        Search for movies by title or overview
        
        Args:
            query (str): Search query
            num_results (int): Number of results to return
            
        Returns:
            pd.DataFrame: Search results
        """
        try:
            if self.movies_df is None:
                return pd.DataFrame()
            
            # Search in title and overview
            title_mask = self.movies_df['title'].str.contains(query, case=False, na=False)
            overview_mask = self.movies_df['overview'].str.contains(query, case=False, na=False)
            
            search_results = self.movies_df[title_mask | overview_mask]
            
            # Sort by rating
            search_results = search_results.sort_values('rating', ascending=False)
            
            # Return top results
            return search_results.head(num_results).reset_index(drop=True)
            
        except Exception as e:
            print(f"Error searching movies: {e}")
            return pd.DataFrame()

