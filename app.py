import streamlit as st
import pandas as pd
import requests
import pickle


with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

    import pickle
import pandas as pd

# movie_data.pkl ki jagah ye dono load karo jo abhi banaye hain
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

cosine_sim = pickle.load(open('similarity.pkl', 'rb'))

def get_recommendations(title, cosine_sim = cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:11] # Get Top 10 Similar Movies
    movie_indices = [i[0] for i in sim_scores]
    
    # Return the full dataframe slice, not just the 'title' column
    return movies.iloc[movie_indices]


# def fetch_poster(movie_id):
#     api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
#     url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
#     response = requests.get(url)
#     data = response.json()
#     poster_path = data['poster_path']
#     full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
#     return full_path

def fetch_poster(movie_title):
    api_key = '259f820f' 
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'
    
    try:
        response = requests.get(url, timeout=3)
        data = response.json()
        
        # OMDb me poster ka key capital 'P' se 'Poster' hota hai
        if data.get('Poster') and data['Poster'] != 'N/A':
            return data['Poster']
        else:
            return "https://via.placeholder.com/130x195?text=No+Poster"
            
    except:
        return "https://via.placeholder.com/130x195?text=Error"

    
    
st.title("Movie Recommendation System")

# Dropdown list
selected_movie = st.selectbox('You choose one. I\'ll give you five. You\'re welcome!!! 😉', movies['title'].values)

if st.button("Recommend"):
    recommendations = get_recommendations(selected_movie)
    st.write("You'll like these too. I mean, I picked 'em.... 😉")
    
    # Create a 2x5 Grid Layout
    for i in range(0, 10, 5):  # Loop over rows (2 rows, 5 movies each)
        cols = st.columns(5)   # Create 5 columns for each row
        
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                # Title nikalna
                movie_title = recommendations.iloc[j]['title']
                
                # Poster ka URL nikalna
                poster_url = fetch_poster(movie_title)
                
                # Column ke andar image aur text dikhana
                with col:
                    st.image(poster_url, width=130) # Ye line posters dikhayegi
                    st.write(movie_title)