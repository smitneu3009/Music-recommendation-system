import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:11]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
    return recommended_music_names, recommended_music_posters

# Load data
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.header('Music Recommender System')

# Initialize session state for selected song
if 'selected_song' not in st.session_state:
    st.session_state.selected_song = None

# Dynamic search input
search_query = st.text_input("Search for a song", key='search_query')

# Filter songs based on search query
filtered_music = music[music['song'].str.contains(search_query, case=False, na=False)] if search_query else music

# Display filtered songs as suggestions
if search_query:
    if not filtered_music.empty:
        suggestions = filtered_music['song'].values[:5]  # Limit to top 5 suggestions
        for song in suggestions:
            if st.button(song):
                st.session_state.selected_song = song
                st.experimental_rerun()
    else:
        st.write("No songs found matching your search.")
        st.session_state.selected_song = None

# Show recommendations for the selected song
if st.session_state.selected_song:
    st.write(f"Selected Song: {st.session_state.selected_song}")
    recommended_music_names, recommended_music_posters = recommend(st.session_state.selected_song)
    for i in range(0, len(recommended_music_names), 5):
        cols = st.columns(5)
        for col, name, poster in zip(cols, recommended_music_names[i:i+5], recommended_music_posters[i:i+5]):
            with col:
                st.text(name)
                st.image(poster)
