import streamlit as st
import random
from qloo_client import get_movies_by_tag
from utils import generate_dramatic_summary, generate_mood_shayari, ask_llm_for_question, infer_genre_from_answers

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

st.markdown('<div class="main-title">🧠 CinePsych - The Movie Mood Reader</div>', unsafe_allow_html=True)

# --- Chat UI functions ---
def show_ai_msg(msg):
    st.markdown(f'<div class="chat-bubble ai-bubble">🤖 {msg}</div>', unsafe_allow_html=True)

def show_user_msg(msg):
    st.markdown(f'<div class="chat-bubble user-bubble">🧑 {msg}</div>', unsafe_allow_html=True)

# --- Session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- Step 0: Choose Bollywood or Hollywood ---
if st.session_state.step == 0:
    show_ai_msg("🎭 Hello! I'm <b>CinePsych</b>, your AI movie mood reader.<br><br>First, tell me — are you into <b>Hollywood</b> or <b>Bollywood</b> vibes today?")
    user = st.chat_input("Type: Hollywood or Bollywood")
    if user:
        show_user_msg(user)
        st.session_state.lang = "Hindi" if "bolly" in user.lower() else "English"
        st.session_state.answers["cinema_type"] = user
        st.session_state.step += 1
        st.rerun()

# --- Steps 1 to 5: Dynamic LLM questions ---
elif st.session_state.step in [1, 2, 3, 4, 5]:
    if len(st.session_state.chat_history) < st.session_state.step:
        with st.spinner("🤔 Thinking of a good question..."):
            q = ask_llm_for_question(st.session_state.answers)
            st.session_state.chat_history.append({"question": q})
            st.rerun()
    else:
        question = st.session_state.chat_history[st.session_state.step - 1]["question"]
        show_ai_msg(question)
        user = st.chat_input("Your reply...")
        if user:
            show_user_msg(user)
            st.markdown('<div class="thinking">🤖 Thinking...</div>', unsafe_allow_html=True)
            st.session_state.answers[f"q{st.session_state.step}"] = user
            st.session_state.step += 1
            st.rerun()

# --- Step 6: Final prediction & movie suggestion ---
elif st.session_state.step == 6:
    with st.spinner("🧠 Reading your mood..."):
        mood_genre = infer_genre_from_answers(st.session_state.answers)
        tag_map = {
            "Drama": "urn:tag:genre:media:drama",
            "Comedy": "urn:tag:genre:media:comedy",
            "Romance": "urn:tag:genre:media:romance",
            "Thriller": "urn:tag:genre:media:thriller",
            "Family": "urn:tag:genre:media:family",
            "Fantasy": "urn:tag:genre:media:fantasy",
            "Adventure": "urn:tag:genre:media:adventure"
        }

        genre_tag = tag_map.get(mood_genre, tag_map["Drama"])
        movies = get_movies_by_tag(genre_tag)

        if not movies or not mood_genre:
            show_ai_msg("😔 Hmm... I'm not feeling quite myself today.<br><br>Would you like to help me feel better?")
            user_response = st.chat_input("Say 'yes' to continue or anything else to exit.")
            if user_response and "yes" in user_response.lower():
                show_user_msg(user_response)
                st.session_state.step = 1
                show_ai_msg("🥹 You're the best. Let’s try again with a fresh perspective...")
                st.rerun()
            else:
                show_user_msg(user_response or "...")
                show_ai_msg("I understand. Let’s chat another time. Take care. 💜")
                st.session_state.step = 999
        else:
            movie = random.choice(movies[:5])
            title = movie.get("name", "Untitled")
            desc = movie.get("properties", {}).get("description", "")
            image = movie.get("properties", {}).get("image", {}).get("url", "https://via.placeholder.com/300")

            poetic_line = generate_dramatic_summary(title, desc)
            shayari = generate_mood_shayari(mood_genre, st.session_state.lang)

            show_ai_msg(f"🎯 Your mood is definitely <b>{mood_genre}</b>.<br>Let me show you a movie that reflects it...")

            # --- Movie card styling ---
            st.markdown("""
                <style>
                    .movie-card {
                        display: flex;
                        flex-wrap: wrap;
                        background-color: #1b1b1b;
                        border-radius: 15px;
                        overflow: hidden;
                        box-shadow: 0 0 15px rgba(255, 102, 204, 0.4);
                        margin-top: 1.5rem;
                    }
                    .movie-poster {
                        width: 200px;
                        height: auto;
                        object-fit: cover;
                        border-right: 2px solid #ff66cc;
                    }
                    .movie-content {
                        flex: 1;
                        padding: 1.2rem;
                        color: #eee;
                    }
                    .movie-title {
                        font-size: 1.5rem;
                        font-weight: bold;
                        color: #ff66cc;
                    }
                    .movie-desc {
                        font-size: 0.95rem;
                        color: #ccc;
                        margin-top: 0.4rem;
                    }
                    .movie-line {
                        font-style: italic;
                        color: #f5f5f5;
                        margin-top: 1rem;
                    }
                    .shayari-block {
                        margin-top: 1rem;
                        color: #aad8ff;
                        font-size: 1rem;
                    }

                    @media screen and (max-width: 768px) {
                        .movie-card {
                            flex-direction: column;
                        }
                        .movie-poster {
                            width: 100%;
                            max-height: 250px;
                        }
                        .movie-content {
                            padding: 1rem;
                        }
                    }
                </style>
            """, unsafe_allow_html=True)

            # --- Render movie suggestion ---
            st.markdown(f"""
                <div class="movie-card">
                    <img class="movie-poster" src="{image}" alt="Movie Poster">
                    <div class="movie-content">
                        <div class="movie-title">🎬 {title}</div>
                        <div class="movie-desc">{desc}</div>
                        <div class="movie-line">💬 {poetic_line}</div>
                        <div class="shayari-block">🪷 Mood Poetry:<br><blockquote>{shayari}</blockquote></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.session_state.step += 1
