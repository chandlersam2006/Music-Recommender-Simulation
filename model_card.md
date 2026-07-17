# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

ChillMachine 1.0
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

This recommender is designed to generate simple music recommendations based on a user's stated preferences for genre, mood, and energy. It assumes that a person's taste can be represented by a few clear preferences and that songs with similar traits will be a good match. The model is mainly intended for classroom exploration, not for real production users, because it works on a very small dataset and uses a simple scoring rule instead of learning from real listening behavior.

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

Answers:

- It generates top-k song recommendations that best match a user's preferred genre, mood, and energy level.
- It assumes users can describe their taste with a small set of stable preferences and that similar songs will be liked.
- This is primarily for classroom exploration, not real-world deployment.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

The model looks at a few features from each song: genre, mood, energy, and some extra metadata like acousticness, tempo, valence, and danceability. For the user, it mainly considers favorite genre, favorite mood, and target energy, then compares those preferences to every song in the catalog. Songs earn points when the genre matches, when the mood matches, and when the energy level is close to what the user wants. My version kept the scoring transparent and easy to explain, so instead of using a complex machine learning model, it ranks songs with a clear point system that shows why one track appears above another.

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Answers:

- Song features used are genre, mood, and energy as core signals, with metadata such as acousticness, tempo, valence, and danceability available in the dataset.
- User preferences considered are favorite genre, favorite mood, and target energy.
- The model compares each song to those preferences and gives higher scores to songs with matching genre/mood and similar energy, then ranks songs from highest to lowest score.
- From the starter version, I focused on keeping the system transparent and explainable, with clear profile comparisons and written evaluation of where the scoring behaves well or shows bias.

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

The dataset contains 18 songs, which is enough to test the recommender but still very small compared to a real music platform. It includes a range of genres and moods such as pop, lofi, rock, ambient, jazz, synthwave, blues, folk, hip-hop, classical, reggae, disco, and country, with moods like happy, chill, intense, relaxed, focused, moody, sad, romantic, confident, melancholic, energetic, and uplifting. I did not remove data, but the catalog is still limited because it does not include many artists, languages, or unusual listening contexts. Important parts of musical taste are also missing, such as lyrics, cultural background, personal memories, and how a person's preferences might change over time.

Prompts:  

- How many songs are in the catalog  13
- What genres or moods are represented  Happy, chill and relaxed
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  No

---

## 5. Strengths  

Where does your system seem to work well  

This system works best for users whose preferences are clear and consistent, especially when they want a specific combination of genre, mood, and energy. It captures the basic pattern that songs should rank higher when they match the user's stated taste profile, and in the sample tests the top recommendations usually felt reasonable for the profile being tested. For example, the Chill Lofi profile produced calm, low-energy tracks like Midnight Coding and Library Rain, while the Deep Intense Rock profile moved toward louder and more aggressive songs like Storm Runner. That made the outputs feel intuitive and showed that the scoring rule can successfully separate different listening styles.

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

Answers:

- It works best for users with clear, consistent preferences (for example, users who strongly prefer one mood and energy range).
- It captures the pattern that songs ranking highest usually share the user's stated mood/genre and sit near their target energy.
- The recommendations matched my intuition when Chill Lofi surfaced calmer tracks and Deep Intense Rock surfaced more aggressive high-energy tracks.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

One weakness I discovered is that the energy scoring can unfairly disadvantage users with very low or very high energy preferences. The model gives fewer points when a song's energy is more than 0.5 away from the user's target, so people with extreme tastes can have many songs effectively ruled out right away. In my experiments, this made the recommender more flexible for mid-range users than for users at the edges of the scale. This creates a bias because the system is better at serving users whose preferences are closer to the middle of the dataset.

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

I tested three user profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock. I looked at whether the top recommendations changed in sensible ways when the preferred genre, mood, and target energy changed, and whether the songs at the top felt musically consistent with each profile. One thing that surprised me was that some songs still ranked fairly well even without a genre match, simply because their energy was very close to the user's target. That showed me the system is responsive to energy, but it also confirmed that energy can sometimes overpower more subtle differences in musical style.

Comparing High-Energy Pop and Chill Lofi, the output shifted from upbeat pop tracks like Sunrise City and Gym Hero toward calmer songs like Midnight Coding, Library Rain, and Focus Flow. That makes sense because the target energy drops from 0.8 to 0.4 and the favorite mood changes from happy to chill, so the recommender starts rewarding lower-energy songs with a softer feel.

Comparing High-Energy Pop and Deep Intense Rock, both profiles still favored high-energy songs, but the top result changed from bright, upbeat pop to heavier tracks like Storm Runner. That difference makes sense because the two profiles are similar in energy but different in genre and mood, so the system separates “happy and energetic” from “intense and energetic.”

Comparing Chill Lofi and Deep Intense Rock, the recommendations changed the most: Chill Lofi preferred mellow and acoustic-feeling songs, while Deep Intense Rock moved toward loud, fast, intense tracks such as Storm Runner and Electronic Dreams. This makes sense because those profiles differ on all three main preferences, so the ranking moves from low-energy chill music to high-energy aggressive music.

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

Answers:

- I tested High-Energy Pop, Chill Lofi, and Deep Intense Rock profiles.
- I looked for whether top songs changed logically when genre, mood, and target energy changed.
- I was surprised that some songs ranked well without genre match when their energy was very close to the target.
- I ran pairwise comparisons across the three profiles to check whether ranking shifts were consistent with the preference changes.

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Future improvements I would prioritize:

- Add more user preference signals such as preferred tempo range, favorite artists, and tolerance for genre mixing.
- Improve recommendation explanations so each result clearly states which preference contributed most and what tradeoffs occurred.
- Add a diversity step to prevent near-duplicate songs from dominating the top results.
- Support more complex tastes by allowing multi-genre preferences and context-aware profiles (for example, study mode vs workout mode).

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
