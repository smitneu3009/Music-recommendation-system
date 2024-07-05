import streamlit as st
import pandas as pd
import pickle
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict

# Spotify API credentials
CLIENT_ID = "617fe5f4a00c4270a155093962ebb04b"
CLIENT_SECRET = "c6e17d9d51d9469a955cfa66fc8dab26"

# Authenticate with Spotify API
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Load the data and similarity matrix from pickle files
with open('df_reduced.pkl', 'rb') as f:
    df = pickle.load(f)

with open('similarity_reduced.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Create the pivot table again
pivot_table = df.pivot_table(index='title', columns='artist', values='streams', aggfunc='sum', fill_value=0)

# Convert the index to lowercase for case-insensitive matching
pivot_table.index = pivot_table.index.str.lower()

# Define the function to recommend songs based on similarity
def recommend_songs(song_title, similarity_matrix, pivot_table):
    song_title = song_title.lower()
    if song_title not in pivot_table.index:
        return ["Song not found in the dataset."]
    
    song_index = pivot_table.index.get_loc(song_title)
    similarity_scores = similarity_matrix[song_index]
    similar_songs = list(enumerate(similarity_scores))
    similar_songs_sorted = sorted(similar_songs, key=lambda x: x[1], reverse=True)
    recommended_song_indices = [x[0] for x in similar_songs_sorted]
    recommended_songs = [pivot_table.index[i] for i in recommended_song_indices if i != song_index]
    
    # Remove duplicates while maintaining order
    unique_recommended_songs = list(OrderedDict.fromkeys(recommended_songs))
    
    return unique_recommended_songs

# Function to get album cover URL from Spotify API or default if not available
def get_album_cover_url(song_title, artist_name):
    query = f"track:{song_title} artist:{artist_name}"
    results = sp.search(q=query, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        if tracks[0]['album']['images']:
            album_cover_url = tracks[0]['album']['images'][0]['url']
        else:
            # Use default Spotify cover image
            album_cover_url = "https://developer.spotify.com/images/guidelines/design/icon4@2x.png"
        return album_cover_url
    # Use default Spotify cover image if no tracks found
    return "https://developer.spotify.com/images/guidelines/design/icon4@2x.png"

# Streamlit app setup
st.set_page_config(page_title='Song Recommendation System', layout='wide')
st.title('Song Recommendation System')
st.write("Enter a song title to get recommendations.")

# Initialize session state for the selected song
if 'selected_song' not in st.session_state:
    st.session_state.selected_song = ''

# User input for song title
song_title = st.text_input('Song Title', value=st.session_state.selected_song)

# Show song suggestions without buttons
selected_suggestion = None
if song_title:
    song_title_lower = song_title.lower()
    suggestions = [title for title in pivot_table.index if song_title_lower in title]
    if suggestions:
        selected_suggestion = st.selectbox("Suggestions:", options=[suggestion.title() for suggestion in suggestions[:10]])

# Recommend songs based on selected suggestion
if st.button('Recommend'):
    if selected_suggestion:
        recommended_songs = recommend_songs(selected_suggestion, similarity, pivot_table)
        st.write(f"Recommended songs for '{selected_suggestion}':")
        cols = st.columns(5)  # Create 5 columns for the grid layout
        for idx, song in enumerate(recommended_songs[:10]):
            # Get artist name for the song
            artist_name = df[df['title'].str.lower() == song].iloc[0]['artist']
            # Get album cover URL
            album_cover_url = get_album_cover_url(song, artist_name)
            col = cols[idx % 5]
            with col:
                st.markdown(
                    f"""
                    <div class="song-title">
                        {song.title()}
                    </div>
                    <img src="{album_cover_url}" class="album-cover">
                    """, unsafe_allow_html=True)

# CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1A1A1A; /* Dark background */
        color: #FFFFFF; /* White text */
    }
    .song-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .album-cover {
        width: 150px;
        height: 150px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True
)
