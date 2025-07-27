import os
import gdown
import streamlit as st
import pickle
import pandas as pd
import requests

# ✅ Google Drive file IDs
movie_dict_id = "1VXtowOumam1yDIK7RCiYDjf9dhUv66wa"
similarity_id = "12ruJiBhb3tV30nMSySNpNxQAI9ofGbbS"

# ✅ Local file paths
movie_dict_path = "movie_dict.pkl"
similarity_path = "similarity.pkl"

# ✅ Download movie_dict.pkl if not exists
if not os.path.exists(movie_dict_path):
    st.info("Downloading movie_dict.pkl...")
    gdown.download(f"https://drive.google.com/uc?id={movie_dict_id}", movie_dict_path, quiet=False)

# ✅ Download similarity.pkl if not exists
if not os.path.exists(similarity_path):
    st.info("Downloading similarity.pkl...")
    gdown.download(f"https://drive.google.com/uc?id={similarity_id}", similarity_path, quiet=False)

# ✅ Load the data
movies_dict = pickle.load(open(movie_dict_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))
movies = pd.DataFrame(movies_dict)

# ✅ TMDb API Key (replace with your key if needed)
API_KEY = "34d236ffd6e1e129ded294bc6345e95d"

# 🎞️ Fetch poster using TMDb
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

# 🎬 Recommend movies
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []
    
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1]()_
