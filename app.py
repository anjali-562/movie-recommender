import streamlit as st
from recommend import recommend

st.title("🎬 Movie Recommender System")
movie = st.text_input("Enter a movie title:")

if st.button("Recommend"):
    with st.spinner("Finding similar movies..."):
        results = recommend(movie)
        st.subheader("Recommended Movies:")
        for i, m in enumerate(results, 1):
            st.write(f"{i}. {m}")
