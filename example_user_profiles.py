"""
Example User Profiles for the Music Recommender System

Each profile is a dictionary with:
- favorite_genre: String matching a genre in the dataset
- favorite_mood: String matching a mood in the dataset
- target_energy: Float 0.0–1.0 (0=calm, 1=intense)
- likes_acoustic: Boolean (True for acoustic, False for electric/produced)
"""

# Profile 1: The Chill Lofi Enthusiast
# "I want background music while I work—mellow, acoustic, and calm"
PROFILE_CHILL_LOFI = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.4,  # Low energy
    "likes_acoustic": True,  # Prefers acoustic
}

# Profile 2: The Intense Rock Fan
# "I want high-energy music with attitude—electric production, fast-paced"
PROFILE_INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.85,  # High energy
    "likes_acoustic": False,  # Prefers electric/produced
}

# Profile 3: The Pop Party Lover
# "I want upbeat, happy music that makes me want to dance"
PROFILE_POP_HAPPY = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.75,  # Medium-high energy
    "likes_acoustic": False,  # Prefers clean/produced pop
}

# Profile 4: The Balanced Listener (RECOMMENDED for your project)
# "I like indie pop with relaxed vibes, not too intense, somewhat acoustic"
# This profile is MODERATE in specificity—not too narrow, not too broad
PROFILE_BALANCED = {
    "favorite_genre": "indie pop",
    "favorite_mood": "happy",
    "target_energy": 0.65,  # Medium energy (NOT extreme)
    "likes_acoustic": True,  # Yes to acoustic, but won't reject electric
}


# CRITIQUE FRAMEWORK
# ===================
# Use these questions to evaluate if a profile is good:

CRITIQUE_QUESTIONS = """
PROFILE CRITIQUE CHECKLIST:

1. DIFFERENTIATION TEST: Can this profile clearly distinguish between opposites?
   ✓ Does it score "Intense Rock" (high energy, electric, intense mood) differently than "Chill Lofi" (low energy, acoustic, chill mood)?
   ✗ If both score similarly, the profile is TOO BROAD (lacks specificity)
   ✗ If one is severely penalized, the profile is TOO NARROW (too extreme)

2. SPECIFICITY TEST: Is the profile specific enough to be realistic?
   ✓ Does it describe a real person's taste (e.g., "I like pop music, happy songs, medium energy")?
   ✗ If it's vague (e.g., "I like good music"), it's TOO BROAD
   ✗ If it's extreme (e.g., "ONLY pop, ONLY happy, MUST be 0.8 energy"), it's TOO NARROW

3. EXTREME vs. MODERATE TEST:
   - Extreme profiles: target_energy at 0.1, 0.9, or 1.0; like/dislike is binary
   - Moderate profiles: target_energy around 0.4–0.7; like/dislike is more forgiving
   
   Moderate profiles typically BETTER differentiate because:
   - They reward "somewhat close" matches (via Gaussian), not just perfect ones
   - They show nuance: "I prefer X, but I'm open to similar things"

4. REAL-WORLD VALIDITY TEST:
   ✓ Would a real person describe their taste this way?
   ✓ Can you find multiple songs in the dataset that match?
   ✗ If no songs match, the profile may be TOO SPECIFIC


RECOMMENDATION FOR YOUR PROJECT:
================================

Use PROFILE_BALANCED (indie pop lover) because:

1. It's DIFFERENTIATED enough:
   - "Intense Rock" scores low (wrong genre, wrong mood, too high energy, electric)
   - "Chill Lofi" scores low (wrong genre, wrong mood, low energy but you want medium)
   - "Indie Pop Happy" scores HIGH (perfect genre match, perfect mood, medium energy OK)

2. It's REALISTIC:
   - A real person could say: "I like indie pop, happy songs, medium energy, with acoustic elements"
   - Not extreme: allows some electric songs to score decently if other attributes match

3. It TESTS THE SCORING RULE:
   - Shows how Gaussian energy proximity works (0.65 target rewards 0.6–0.7, slightly rewards 0.5–0.8)
   - Shows how mood/genre matching creates clear differentiation
   - Shows how acoustic preference acts as a tie-breaker

4. It's NOT TOO NARROW:
   - A song with different genre but perfect mood/energy might still score OK
   - Allows the recommender to show "diversification" in recommendations
"""

print(CRITIQUE_QUESTIONS)

# SCORING EXAMPLE
# ===============
# If you want to manually test how these profiles score real songs:

EXAMPLE_SONGS_FOR_TESTING = {
    "Storm Runner": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.91,
        "acousticness": 0.10,
    },
    "Library Rain": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "acousticness": 0.86,
    },
    "Rooftop Lights": {
        "genre": "indie pop",
        "mood": "happy",
        "energy": 0.76,
        "acousticness": 0.35,
    },
}

# To score manually, you would calculate:
# score = 0.40 * genre_score + 0.25 * mood_score + 0.25 * energy_score + 0.10 * acoustic_score
#
# For PROFILE_BALANCED scoring "Rooftop Lights":
# - genre_score = 1.0 (perfect match: indie pop == indie pop)
# - mood_score = 1.0 (perfect match: happy == happy)
# - energy_score = exp(-5 * (0.76 - 0.65)^2) = exp(-5 * 0.0121) ≈ 0.94 (close!)
# - acoustic_score = 0.35 (some acoustic, but user prefers more; 1 - 0.35 would be 0.65 if inverted)
#   Actually: likes_acoustic=True, so acoustic_score = acousticness = 0.35
# - total = 0.40 * 1.0 + 0.25 * 1.0 + 0.25 * 0.94 + 0.10 * 0.35
#         = 0.40 + 0.25 + 0.235 + 0.035 = 0.92 ✓✓✓ EXCELLENT MATCH
#
# For PROFILE_BALANCED scoring "Storm Runner":
# - genre_score = 0.3 (rock != indie pop, so penalty)
# - mood_score = 0.5 (intense != happy, partial credit)
# - energy_score = exp(-5 * (0.91 - 0.65)^2) = exp(-5 * 0.0676) ≈ 0.72 (moderate, too high)
# - acoustic_score = 0.10 (very electric, but user likes acoustic; this is penalized)
# - total = 0.40 * 0.3 + 0.25 * 0.5 + 0.25 * 0.72 + 0.10 * 0.10
#         = 0.12 + 0.125 + 0.18 + 0.01 = 0.435 ✗ POOR MATCH (should rank low)
