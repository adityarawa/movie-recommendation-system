import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    )
    if response.status_code == 200:
        data = response.json()
        if "poster_path" in data:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            print(f"Error: 'poster_path' not found for movie ID {movie_id}")
            return None
    else:
        print(f"Error fetching movie data: {response.text}")
        return None

def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    recommended_posters = [fetch_poster(movies.iloc[i[0]].id) for i in movies_list]
    return recommended_movies, recommended_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select a Movie', movies['title'].values)

if st.button('Recommend'):
    recommended_movies, recommended_posters = recommend(selected_movie_name)

    # Improved layout for displaying recommendations
    col1, col2 = st.beta_columns(2)
    for i in range(2):
        with col1:
            st.text(recommended_movies[i])
            if recommended_posters[i]:
                st.image(recommended_posters[i])
        col1.empty()  # Add spacing between movies

    col3, col4, col5 = st.beta_columns(3)
    for i in range(2, 5):
        with col3:
            st.text(recommended_movies[i])
            if recommended_posters[i]:
                st.image(recommended_posters[i])
        col3.empty()  # Add spacing between movies