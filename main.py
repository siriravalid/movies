import streamlit as st
import pickle
import bz2
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load model data from the .pkl.bz2 file
def load_model_and_data():
    model_path = 'model_data.pkl.bz2'
    try:
        with bz2.BZ2File(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"Error loading model data: {e}")
        return None

model_data = load_model_and_data()
if model_data is None:
    st.stop()

# Unpack the model data
similarity = model_data['similarity']
movies_data = model_data['movies_data']

# Streamlit application
st.title('Movie Recommendation System')

# User input
movie_name = st.text_input('Enter your favourite movie name:')

if movie_name:
    # Find close match for the movie name
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    
    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        
        # Get similarity scores
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        
        # Display recommendations
        st.write('Movies suggested for you:')
        for i, movie in enumerate(sorted_similar_movies):
            index = movie[0]
            title_from_index = movies_data[movies_data.index == index]['title'].values[0]
            if i < 30:
                st.write(f"{i + 1}. {title_from_index}")
    else:
        st.write("Movie not found. Please try another one.")
