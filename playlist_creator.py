from spotify_client import SpotifyClient
from sentiment_analysis import SentimentAnalysis
import ollama
import time
import random
import re
import json

class PlaylistCreator:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client
        self.analyzer = SentimentAnalysis()

    def generate_playlist_name(self, mood):
        """Ensures each playlist has a unique and clean name using an LLM with JSON output formatting."""
        timestamp = time.strftime("%H:%M:%S")  
        prompt = (
            f"Generate three unique, creative, and meaningful playlist names based on the mood '{mood}'. "
            "The names should make sense, be readable, and use common words. "
            "Avoid nonsense words, special characters (except emojis), or gibberish. "
            "Use real words and phrases that could exist in English. "
            "Return the names as a JSON array in the following format: "
            "[{\"Suggestion\": \"Name 1\"}, {\"Suggestion\": \"Name 2\"}, {\"Suggestion\": \"Name 3\"}]. "
            "Ensure each title is under 100 characters and properly formatted."
        )

        response = ollama.chat(model='mistral', messages=[{"role": "user", "content": prompt}])
        raw_output = response['message']['content'].strip()

        try:
            # Parse JSON output
            suggestions = json.loads(raw_output)
            
            # Extract and clean playlist names
            cleaned_suggestions = [
                re.sub(r"[^a-zA-Z0-9\s\!\?\.,'🤘🎶🔥🌊☀️🎧💃🕺🎸]", "", s["Suggestion"]).strip()
                for s in suggestions if "Suggestion" in s
            ]
            
            # Filter out empty or malformed suggestions
            cleaned_suggestions = [s for s in cleaned_suggestions if s and len(s) > 3]
            
            if not cleaned_suggestions:
                return "Mood Vibes 🎵"  # Default fallback
            
            # Select a random suggestion
            chosen_name = random.choice(cleaned_suggestions)
            
            # Ensure playlist name does not exceed 100 characters
            return chosen_name[:100]  # Truncate if necessary
        
        except (json.JSONDecodeError, KeyError, TypeError):
            return "Mood Vibes 🎵"  # Fallback if JSON parsing fails
    
    def create_mood_playlist(self, mood_text):
        # Analyze mood and get genres
        mood, intensity = self.analyzer.analyze_sentiment(mood_text)
        genres = self.analyzer.get_genres_for_mood(mood, intensity)
        
        # Search for tracks
        tracks = self.spotify_client.search_tracks(genres, limit=10)
        
        # Generate a creative playlist name using Ollama and mistral model
        playlist_name = self.generate_playlist_name(mood_text)
        playlist_description = f"A playlist to match your {mood_text} mood with {', '.join(genres)} vibes."
        playlist_id = self.spotify_client.create_playlist(playlist_name, playlist_description)
        
        # Add tracks to the playlist
        self.spotify_client.add_tracks_to_playlist(playlist_id, tracks)
        
        print(f"Created playlist: {playlist_name} with {len(tracks)} tracks!")
    

    

  
      
