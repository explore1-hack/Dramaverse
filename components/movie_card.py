# components/movie_card.py

import streamlit as st
from utils import extract_property, safe_image, get_aka_titles

def display_movie(movie, dramatic_line=None):
    title = movie.get("name", "Untitled")
    description = extract_property(movie, "description", "No description available.")
    year = extract_property(movie, "release_year", "Unknown")
    rating = extract_property(movie, "content_rating", "N/A")
    aka_titles = get_aka_titles(movie)
    image_url = safe_image(movie)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(image_url, width=220)

    with col2:
        st.markdown(f"### 🎬 {title} ({year})")
        st.markdown(f"**📜 AKA:** `{', '.join(aka_titles[:3])}`" if aka_titles else "")
        st.markdown(f"**🔞 Rating:** `{rating}`")
        st.write(description)

        if dramatic_line:
            st.markdown(f"💬 _{dramatic_line}_")

    st.markdown("---")
