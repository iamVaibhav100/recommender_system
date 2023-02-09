import os
from dotenv import load_dotenv

import streamlit as st
import pickle
import pandas as pd
import requests

load_dotenv()
api = os.getenv("API_KEY")


def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api}&language=en-US"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for movie in movies_list:
        movie_id = movies.iloc[movie[0]].movie_id
        recommended_movies.append(movies.iloc[movie[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open("movies.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))


st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    'Which movie would you like to get recommendations for?',
    movies['title'].values)

if st.button('Show recommendations'):
    st.text(f"Recommendations for {selected_movie_name}")
    st.image(fetch_poster(movies[movies['title'] == selected_movie_name].movie_id.values[0]))
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
