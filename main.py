import streamlit as st
import pickle
import difflib

# Load the model and data
with open('movie_recommender.sav', 'rb') as model_file:
    similarity, movies_data = pickle.load(model_file)

# Function to recommend movies
def recommend_movies(movie_name, similarity, movies_data):
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    
    if find_close_match:
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        
        recommended_movies = []
        for i in range(1, 30):
            index = sorted_similar_movies[i][0]
            title_from_index = movies_data.loc[index, 'title']
            recommended_movies.append(title_from_index)
        
        return recommended_movies
    else:
        return ["No match found"]

# Streamlit app
st.title("Movie Recommendation System")
movie_name = st.text_input("Enter your favourite movie name:")

if st.button("Recommend"):
    if movie_name:
        recommended_movies = recommend_movies(movie_name, similarity, movies_data)
        st.write("Movies suggested for you:\n")
        for i, title in enumerate(recommended_movies):
            st.write(f"{i+1}. {title}")
    else:
        st.write("Please enter a movie name.")
