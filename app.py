
import streamlit as st
import random
from qloo_client import get_movies_by_tag
from utils import generate_dramatic_summary, generate_mood_shayari, ask_llm_for_question, infer_genre_from_answers, guess_movie_from_description

import base64
from pathlib import Path

# --- Background Image Setup ---
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        body {{
            background-image: url("data:assets/background.png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stAppViewContainer"] {{
            background-color: rgba(0, 0, 0, 0.6);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

add_bg_from_local("background-min.png")

# --- Responsive Styling ---
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: bold;
        margin-top: -10px;
        color: #ff66cc;
        text-align: center;
    }

    .chat-bubble {
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem auto;
        background-color: #1e1e1e;
        color: #fff;
        max-width: 90%;
        box-shadow: 0 0 8px #ff69b4;
        font-size: 1rem;
    }
    .user-bubble {
        background-color: #292929;
        border-left: 5px solid #ff66cc;
    }
    .ai-bubble {
        background-color: #333;
        border-left: 5px solid #4fc3f7;
    }
    .thinking {
        font-style: italic;
        color: #aaa;
        text-align: center;
        padding-top: 0.5rem;
    }

    @media screen and (max-width: 768px) {
        .main-title { font-size: 1.6rem; }
        .chat-bubble { font-size: 0.95rem; }
        .movie-title { font-size: 1.2rem !important; }
        .movie-desc { font-size: 0.85rem !important; }
        .shayari-block { font-size: 0.9rem !important; }
        .movie-line { font-size: 0.9rem !important; }
        .movie-poster { width: 120px !important; }
    }
    </style>
""", unsafe_allow_html=True)
