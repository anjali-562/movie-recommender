import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load and merge data
movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")
movies = movies.merge(credits, on='title')
movies = movies[['movie_id', 'title', 'overview', 'genres', 'vote_average']].dropna()

# Extract genres
def extract_genres(x):
    import ast
    return [i['name'] for i in ast.literal_eval(x)]

movies['genres_list'] = movies['genres'].apply(extract_genres)

# TF-IDF similarity
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['overview'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Poster fetcher
def fetch_poster(movie_id):
    try:
        api_key = 'c23e2410f95ad16e1a9150f231529ef7'  # ⬅️ Replace this
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f'https://image.tmdb.org/t/p/w500{poster_path}'
    except Exception as e:
        print("❌ Poster fetch failed:", e)
    return "https://via.placeholder.com/300x450?text=No+Image"

# Content-based recommendation
def recommend(title, genre_filter=None, num=5):
    if title not in indices:
        return []

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    recommended = []
    for i in sim_scores[1:]:
        movie = movies.iloc[i[0]]
        if genre_filter and genre_filter not in movie['genres_list']:
            continue
        recommended.append({
            'title': movie['title'],
            'rating': movie['vote_average'],
            'genres': movie['genres_list'],
            'overview': movie['overview'],
            'poster': fetch_poster(movie['movie_id']),
        })
        if len(recommended) >= num:
            break
    return recommended
