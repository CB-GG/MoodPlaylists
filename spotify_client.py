import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

class SpotifyClient:
    def __init__(self, client_id, client_secret, redirect_uri, scope="playlist-modify-public"):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope
        ))

    def get_user_id(self):
        """Fetch the authenticated Spotify user ID."""
        return self.sp.me()['id']

    def search_tracks(self, genres, limit=10):
        """Enhances diversity by shuffling genres and avoiding repeated songs."""
        all_tracks = []
        searched_tracks = set()
        random.shuffle(genres)  # Randomize the genre order

        for genre in genres:
            results = self.sp.search(q=f'genre:"{genre}"', limit=50, type='track')  # Increase search pool
            unique_tracks = [track['uri'] for track in results['tracks']['items'] if track['uri'] not in searched_tracks]
            searched_tracks.update(unique_tracks)  # Keep track of seen songs
            all_tracks.extend(unique_tracks)

        random.shuffle(all_tracks)  # Shuffle the final selection for variety
        return all_tracks[:limit]  # Return a diverse subset

    def create_playlist(self, name, description=""):
        """Create a new playlist under the authenticated user's account."""
        user_id = self.get_user_id()
        playlist = self.sp.user_playlist_create(user=user_id, name=name, public=True, description=description)
        return playlist['id']

    def add_tracks_to_playlist(self, playlist_id, track_uris):
        """Add tracks to the playlist."""
        self.sp.playlist_add_items(playlist_id, track_uris)

