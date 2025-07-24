# pages/1_Drama.py

import streamlit as st
from qloo_client import get_movies_by_tag
from components.movie_card import display_movie
from utils import generate_dramatic_summary

st.set_page_config(page_title="Comedy Picks 😂", layout="centered")
st.title("🎭 Top Drama Picks")

genre_tag = "urn:tag:genre:media:comedy"

with st.spinner("Fetching emotional dramas..."):
    movies = get_movies_by_tag(genre_tag)

if not movies:
    st.error("No drama movies found.")
else:
    for movie in movies[:6]:
        title = movie.get("name", "Untitled")
        desc = movie.get("properties", {}).get("description", "")
        dramatic_line = generate_dramatic_summary(title, desc)
        display_movie(movie, dramatic_line)
