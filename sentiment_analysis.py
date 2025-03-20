from transformers import pipeline
import random

class SentimentAnalysis:
    def __init__(self):
        # Load a multi-emotion model
        self.analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)

        # Mood-to-genre mapping with intensities
        self.mood_to_genre = {
            "joy": ["pop", "dance", "upbeat"],
            "contentment": ["acoustic", "folk", "chill"],
            "relaxation": ["lofi", "ambient", "jazz"],
            "excitement": ["edm", "party", "electropop"],
            "nostalgia": ["classic rock", "retro", "80s"],
            "sadness": ["blues", "indie", "slowcore"],
            "anxiety": ["trip-hop", "darkwave", "industrial"],
            "anger": ["metal", "hard rock", "punk"],
            "reflection": ["classical", "instrumental", "ambient"],
            "love": ["romantic", "r&b", "soul"],
            "surprise": ["experimental", "electronic", "alt"],
        }

    def analyze_sentiment(self, mood_text):
        # Run sentiment analysis
        results = self.analyzer(mood_text)[0]

        # Extract emotions and their scores
        emotions = {result['label']: result['score'] for result in results}
        primary_emotion = max(emotions, key=emotions.get)
        intensity = emotions[primary_emotion]

        return primary_emotion, intensity

    def get_genres_for_mood(self, mood, intensity):
            """Vary genres slightly each time even for the same mood."""
            primary_genres = self.mood_to_genre.get(mood, ["indie"])

            # Introduce randomization by shuffling and picking different genres each time
            random.shuffle(primary_genres)
            extra_genres = ["jazz", "synthwave", "classical", "chillwave", "psychedelic", "folk"]
            random.shuffle(extra_genres)

            if intensity > 0.75:
                return primary_genres[:2] + extra_genres[:2]  # High energy, mix more genres
            elif intensity < 0.3:
                return primary_genres[:1] + extra_genres[:1]  # Calmer, mix less
            else:
                return primary_genres[:2] + extra_genres[:1]  # Balanced 



