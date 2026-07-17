"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


HIGH_ENERGY_POP = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "likes_acoustic": False,
}

CHILL_LOFI = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.4,
    "likes_acoustic": True,
}

DEEP_INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.9,
    "likes_acoustic": False,
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_profiles = [
        ("High-Energy Pop", HIGH_ENERGY_POP),
        ("Chill Lofi", CHILL_LOFI),
        ("Deep Intense Rock", DEEP_INTENSE_ROCK),
    ]

    for profile_name, user_prefs in user_profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n{profile_name}:\n")
        for index, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            print(f"{index}. {song['title']}")
            print(f"   Score: {score:.2f}")
            print("   Why:")
            for reason in explanation.splitlines():
                print(f"      - {reason}")
            print()

    print("\nTop recommendations:\n")
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{index}. {song['title']}")
        print(f"   Score: {score:.2f}")
        print("   Why:")
        for reason in explanation.splitlines():
            print(f"      - {reason}")
        print()


if __name__ == "__main__":
    main()
