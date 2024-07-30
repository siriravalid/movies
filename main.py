import pickle
import bz2
import pandas as pd
import difflib
import streamlit as st

# Load the compressed model and data
def load_model_and_data():
    with bz2.BZ2File('model_data.pkl.bz2', 'rb') as f:
        model_data = pickle.load(f)
    return model_data

# Streamlit application
st.title('Movie Recommendation System')

# Load model and data
model_data = load_model_and_data()
movies_data = model_data['movies_data']
feature_vectors = model_data['feature_vectors']
similarity = model_data['similarity']

# User input
movie_name = st.text_input('Enter your favourite movie name:')
if movie_name:
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    
    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        
        st.write('Movies suggested for you:')
        for i, movie in enumerate(sorted_similar_movies[:30], start=1):
            index = movie[0]
            title_from_index = movies_data[movies_data.index == index]['title'].values[0]
            st.write(f"{i}. {title_from_index}")
    else:
        st.write("No close match found for the given movie name.")
