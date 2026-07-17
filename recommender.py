import math
import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


def _get_user_preference(user_prefs: Dict, key: str, fallback_key: Optional[str] = None):
    """Return a user preference using either the new or legacy key name."""
    if key in user_prefs:
        return user_prefs[key]
    if fallback_key and fallback_key in user_prefs:
        return user_prefs[fallback_key]
    return None

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Scores all songs and returns top-k ranked by score (descending).
        Implements the Ranking Rule: applies scoring to all songs, then sorts.
        """
        # Apply scoring rule to all songs
        scored_songs = [
            (song, self._score_song(user, song))
            for song in self.songs
        ]
        
        # Ranking rule: sort by score (descending), keeping original order for ties
        ranked = sorted(scored_songs, key=lambda x: x[1], reverse=True)
        
        # Return top-k songs
        return [song for song, score in ranked[:k]]

    def _score_song(self, user: UserProfile, song: Song) -> float:
        """
        Internal helper: scores a single song with a simple point-based recipe.

        Recipe:
        - +2.0 points for an exact genre match
        - +1.0 point for an exact mood match
        - Energy similarity points based on closeness to the target energy
        """
        genre_points = 1.0 if song.genre == user.favorite_genre else 0.0
        mood_points = 1.0 if song.mood == user.favorite_mood else 0.0

        energy_diff = abs(song.energy - user.target_energy)
        energy_points = max(0.0, 1.0 - (energy_diff / 0.5)) * 2.0

        return genre_points + mood_points + energy_points

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explains why a song was recommended by breaking down its score components.
        """
        genre_points = 1.0 if song.genre == user.favorite_genre else 0.0
        mood_points = 1.0 if song.mood == user.favorite_mood else 0.0
        energy_diff = abs(song.energy - user.target_energy)
        energy_points = max(0.0, 1.0 - (energy_diff / 0.5)) * 2.0

        final_score = self._score_song(user, song)

        explanation = f"🎵 {song.title} by {song.artist} (Score: {final_score:.2f})\n"
        explanation += f"  • Genre: +1.0 point - {'match' if song.genre == user.favorite_genre else 'no match'}\n"
        explanation += f"  • Mood: +1.0 point - {'match' if song.mood == user.favorite_mood else 'no match'}\n"
        explanation += f"  • Energy: +{energy_points:.2f} points - target is {user.target_energy:.2f}, song is {song.energy:.2f}"

        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dictionaries."""
    songs = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields to float
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness']),
                }
                songs.append(song)
        print(f"✓ Loaded {len(songs)} songs from {csv_path}")
    except FileNotFoundError:
        print(f"✗ Error: File not found at {csv_path}")
    except Exception as e:
        print(f"✗ Error loading songs: {e}")
    
    return songs

def _score_song_functional(user_prefs: Dict, song: Dict) -> float:
    """Score a single song with the same point-based recipe used by the main recommender."""
    favorite_genre = _get_user_preference(user_prefs, 'favorite_genre', 'genre')
    favorite_mood = _get_user_preference(user_prefs, 'favorite_mood', 'mood')
    target_energy = _get_user_preference(user_prefs, 'target_energy', 'energy')

    genre_points = 1.0 if song['genre'] == favorite_genre else 0.0
    mood_points = 1.0 if song['mood'] == favorite_mood else 0.0

    energy_diff = abs(song['energy'] - target_energy)
    energy_points = max(0.0, 1.0 - (energy_diff / 0.5)) * 2.0

    return genre_points + mood_points + energy_points


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return a numeric score and human-readable reasons for how a song matches a user profile."""
    favorite_genre = _get_user_preference(user_prefs, 'favorite_genre', 'genre')
    favorite_mood = _get_user_preference(user_prefs, 'favorite_mood', 'mood')
    target_energy = _get_user_preference(user_prefs, 'target_energy', 'energy')

    genre_points = 1.0 if song.get('genre') == favorite_genre else 0.0
    mood_points = 1.0 if song.get('mood') == favorite_mood else 0.0

    energy_diff = abs(song.get('energy', 0.0) - target_energy)
    energy_points = max(0.0, 1.0 - (energy_diff / 0.5)) * 2.0

    score = genre_points + mood_points + energy_points

    reasons = []
    if genre_points > 0:
        reasons.append(f"genre match (+{genre_points:.1f})")
    else:
        reasons.append(f"genre mismatch (+{genre_points:.1f})")

    if mood_points > 0:
        reasons.append(f"mood match (+{mood_points:.1f})")
    else:
        reasons.append(f"mood mismatch (+{mood_points:.1f})")

    reasons.append(f"energy similarity (+{energy_points:.2f})")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank them, and return the top-k recommendations for a user."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = f"{song['title']} - {song['artist']}\n" + "\n".join(f"  {r}" for r in reasons)
        scored_songs.append((song, score, explanation))

    ranked = sorted(scored_songs, key=lambda item: item[1], reverse=True)
    return ranked[:k]
