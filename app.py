import os
import gdown
import streamlit as st
import pickle
import pandas as pd
import requests

# === Google Drive File IDs ===
SIMILARITY_ID = "12ruJiBhb3tV30nMSySNpNxQAI9ofGbbS"
MOVIE_DICT_ID = "1VXtowOumam1yDIK7RCiYDjf9dhUv66wa"

# === Download Files ===
def download_file(file_id, output_path):
    if not os.path.exists(output_path):
        print(f"Downloading {output_path}...")
        gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=False)

download_file(SIMILARITY_ID, "similarity.pkl")
download_file(MOVIE_DICT_ID, "movie_dict.pkl")

# === Load Files ===
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

with open("movie_dict.pkl", "rb") as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)

# === API Key ===
API_KEY = "34d236ffd6e1e129ded294bc6345e95d"

# === Fetch Poster ===
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        pass
    return "https://via.placeholder.com/500x750.png?text=No+Poster"

# === Recommend Function ===
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# === Streamlit UI ===
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎥 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if names:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
    else:
        st.error("Movie not found in the database.")

