import streamlit as st
from recommend import recommend, movies

# Setup
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Session for favorites
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# Theme toggle
theme = st.sidebar.selectbox("🎨 Choose Theme", ["Dark", "Light"])

def set_theme(theme):
    if theme == "Dark":
        st.markdown("""
            <style>
                body { background-color: #0E1117; color: white; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body { background-color: #FFFFFF; color: black; }
            </style>
        """, unsafe_allow_html=True)

set_theme(theme)

st.title("🎥 Movie Recommender System")

# Sidebar Filters
st.sidebar.header("🔍 Search & Filter")
movie_list = movies['title'].values
selected_movie = st.sidebar.selectbox("🎬 Choose a Movie", movie_list)

genre_options = sorted(set(g for sublist in movies['genres_list'] for g in sublist))
selected_genre = st.sidebar.selectbox("🎭 Filter by Genre (optional)", [""] + genre_options)

top_n = st.sidebar.slider("🔢 Number of Recommendations", 1, 20, 5)

# Recommend button
if st.sidebar.button("Recommend"):
    with st.spinner("🔎 Finding movies..."):
        results = recommend(selected_movie, genre_filter=selected_genre or None, num=top_n)

    if not results:
        st.error("No recommendations found.")
    else:
        st.subheader(f"📌 Recommendations for *{selected_movie}*")
        for movie in results:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(movie['poster'], use_column_width=True)
            with col2:
                st.markdown(f"### {movie['title']}")
                st.write(f"⭐ **Rating:** {movie['rating']}")
                st.write(f"🎭 **Genres:** {', '.join(movie['genres'])}")
                st.write(f"📝 {movie['overview'][:300]}...")

                fav_key = f"fav_{movie['title']}"
                if st.button("❤️ Add to Favorites", key=fav_key):
                    st.session_state["favorites"].append(movie)
                    st.success(f"Added {movie['title']} to favorites!")

            st.markdown("---")

# Show favorites
with st.expander("📌 View Favorites"):
    if st.session_state["favorites"]:
        for fav in st.session_state["favorites"]:
            st.markdown(f"**{fav['title']}** — ⭐ {fav['rating']}")
    else:
        st.info("No favorites yet!")
