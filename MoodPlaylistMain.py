from sentiment_analysis import SentimentAnalysis
from spotify_client import SpotifyClient
from playlist_creator import PlaylistCreator
import os

class MoodPlaylistGenerator:
    def __init__(self):
        # Get credentials from environment variables 
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

        self.spotify_client = SpotifyClient(client_id, client_secret, redirect_uri)
        self.playlist_creator = PlaylistCreator(self.spotify_client)

    def get_user_input(self):
        """Accept user input for mood description."""
        mood_text = input("Describe your mood: ")
        return mood_text

    def run(self):
        mood_text = self.get_user_input()
        self.playlist_creator.create_mood_playlist(mood_text)

if __name__ == "__main__":
    generator = MoodPlaylistGenerator()
    generator.run()
