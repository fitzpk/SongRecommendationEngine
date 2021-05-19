# Song Recommendation Engine

**Created in collaboration with Ken Duthie**

This project utilizes the Turicreate Python library to create an item-content similarity recommender. To train and test the recommender, a local library of 10,005 songs was used. Audio metrics and metadata information for each song was then extracted using librosa and tiny tag respectively. For a full list of features, please see below.

Features:
- duration of album on which the song appeared
- song duration
- year released
- genre
- audio offset
- bitrate
- sample rate
- tempo
- tuning
- zero crossing rate
- spectral centroid
- spectral bandwidth
- spectral rolloff
- chroma frequency


<br>

**Visuals (just for fun)**

- A <a href="https://fitzpk.github.io/SongRecommendationEngine/artistnetwork.html">D3 visualization</a> was created with the concept that user's should be able to see how their recommended artists are connected.
- A simple <a href="https://public.tableau.com/profile/kevin8018#!/vizhome/SRE_Treemap/TreemapStory">tableau story</a> using treemaps was created to visualize the recommendation reach artists have in total and per song. This gives us a sense of who the most recommended artists are and therefore have the most reach in the database.


