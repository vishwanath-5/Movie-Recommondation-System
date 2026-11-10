import streamlit as st
import pickle
import pandas as pd
import requests
import time

# def fetch_poster(movie_id):
#     url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8133ba4cf44837307bce5032a7825632'
#     response = requests.get(url)
#     data = response.json()
#     return 'https://image.tmdb.org/t/p/original/'+data['poster_path']
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8133ba4cf44837307bce5032a7825632"
#     try:
#         response = requests.get(url, timeout=10)
#         data = response.json()
#         return "https://image.tmdb.org/t/p/w500" + data['poster_path']
#     except requests.exceptions.RequestException:
#         return "https://placehold.co/500x750?text=No+Poster"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8133ba4cf44837307bce5032a7825632"
    for attempt in range(2):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
            return "https://placehold.co/500x750?text=No+Poster"
        except requests.exceptions.RequestException:
            time.sleep(1)
    return "https://placehold.co/500x750?text=Poster+Unavailable"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pd.read_pickle(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Enter your thought please: ",
    movies['title'].values
)

if st.button("Recommend"):
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