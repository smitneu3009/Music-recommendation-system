import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict
import pickle
import re
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

df = pd.read_csv(r"/Users/smit/Downloads/charts.csv")

df = df.iloc[:1000000]

df = df.dropna()

df['date'] = pd.to_datetime(df['date'], errors='coerce')

df['popularity'] = df['streams'] / df['rank']

def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False

df = df[df['title'].apply(is_english)]

def has_long_brackets(text):
    return bool(re.search(r'\[.{10,}\]|\(.{10,}\)', text))

df = df[~df['title'].apply(has_long_brackets)]

pivot_table = df.pivot_table(index='title', columns='artist', values='streams', aggfunc='sum', fill_value=0)

scaler = StandardScaler()
pivot_table_scaled = scaler.fit_transform(pivot_table)

svd = TruncatedSVD(n_components=50, random_state=42)
latent_matrix = svd.fit_transform(pivot_table_scaled)

similarity = cosine_similarity(latent_matrix)

def recommend_songs(song_title, similarity_matrix, pivot_table):
    if song_title not in pivot_table.index:
        print(f"'{song_title}' not found in the dataset.")
        return []
    
    song_index = pivot_table.index.get_loc(song_title)
    similarity_scores = similarity_matrix[song_index]
    similar_songs = list(enumerate(similarity_scores))
    similar_songs_sorted = sorted(similar_songs, key=lambda x: x[1], reverse=True)
    recommended_song_indices = [x[0] for x in similar_songs_sorted]
    recommended_songs = [pivot_table.index[i] for i in recommended_song_indices if i != song_index]
    
    unique_recommended_songs = list(OrderedDict.fromkeys(recommended_songs))
    
    return unique_recommended_songs

song_title = "Safari"

if song_title in pivot_table.index:
    recommended_songs = recommend_songs(song_title, similarity, pivot_table)
    if recommended_songs:
        print(f"Recommended songs for '{song_title}':")
        print(recommended_songs[:10])
else:
    print(f"'{song_title}' not found in the dataset.")

with open('df_reduced.pkl', 'wb') as f:
    pickle.dump(df, f)

with open('similarity_reduced.pkl', 'wb') as f:
    pickle.dump(similarity, f)
