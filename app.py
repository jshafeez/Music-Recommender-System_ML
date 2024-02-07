import os
import pickle
import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials (consider using environment variables)
CLIENT_ID = "553c504d543b4756bb8215220cbd2634"
CLIENT_SECRET = "eac06410430d4439be8dda674974c300"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url, track['preview_url']
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png", None

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_music_previews = []

    for i in distances[1:6]:
        # Fetch the Music poster and preview
        artist = music.iloc[i[0]].artist
        poster, preview = get_song_album_cover_url(music.iloc[i[0]].song, artist)
        recommended_music_posters.append(poster)
        recommended_music_previews.append(preview)
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters, recommended_music_previews

# Load your DataFrame using pandas
music = pd.read_pickle('df.pkl')
similarity = pd.read_pickle('similarity.pkl')

# Set the background color
st.markdown(
    """
    <style>
    body {
        background-color: 000000;
        color: black ;
        font-family: 'Helvetica', sans-serif;
    }
    h1 {
        color: #1DB954;  /* Green color */
        text-align: center;
    }
    .recommendation-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        margin-top: 20px;
    }
    .music-card {
        text-align: center;
        margin-bottom: 20px;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #282828;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Green-colored title
st.title('Music Recommender System')
music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters, recommended_music_previews = recommend(selected_song)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        with col1 if i == 0 else col2 if i == 1 else col3 if i == 2 else col4 if i == 3 else col5:
            st.text(recommended_music_names[i])
            st.image(recommended_music_posters[i])
            if recommended_music_previews[i]:
                st.audio(recommended_music_previews[i], format='audio/ogg', start_time=30)  # Adjust start_time as needed
