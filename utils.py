import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# ----------------- Core LLM Call ------------------

def call_llm(prompt):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "user", "content": prompt.strip()}
        ],
        "temperature": 0.8,
        "top_p": 0.9,
        "max_tokens": 100
    }

    try:
        response = requests.post(TOGETHER_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"💬 LLM Error: {str(e)}"

# ----------------- Smart Questions ------------------

def ask_llm_for_question(prev_answers):
    prompt = f"""
You're an emotional AI movie companion.
Generate one fun, mood-revealing question to ask the user based on their previous responses:

{prev_answers}

Ask something creative (not yes/no) that helps guess user's mood or genre preference.
Make it interactive, like "Pick one...", "Describe...", etc.
Only output the question.
"""
    return call_llm(prompt)

# ----------------- Genre Inference ------------------

def infer_genre_from_answers(answers):
    text = " ".join(answers.values()).lower()
    if "red" in text or "ninjas" in text:
        return "Thriller"
    if "blue" in text or "rain" in text:
        return "Drama"
    if "green" in text or "fantasy" in text:
        return "Fantasy"
    if "love" in text or "romance" in text:
        return "Romance"
    if "funny" in text or "laugh" in text:
        return "Comedy"
    return "Drama"

# ----------------- Poetic Responses ------------------

def generate_mood_shayari(mood, lang="English"):
    prompt = f"""
You are a poetic movie companion. Write a 2-line {'Hindi shayari' if lang=='Hindi' else 'English poem'} about someone feeling {mood}.
Make it emotional and cinematic.
"""
    return call_llm(prompt)

def generate_dramatic_summary(title, description):
    prompt = f"""
You're a poetic film critic.
Write a dramatic one-liner that emotionally describes the movie '{title}'.

Movie Description:
{description}

One-liner:
"""
    return call_llm(prompt)

# ----------------- Basic Movie Info Helpers ------------------

def extract_property(movie, key, default="Not available"):
    return movie.get("properties", {}).get(key, default)

def format_urn_tag(urn):
    if not urn or ":" not in urn:
        return urn
    return urn.split(":")[-1].replace("_", " ").title()

def safe_image(movie):
    return movie.get("properties", {}).get("image", {}).get("url", "https://via.placeholder.com/150")

def get_aka_titles(movie):
    return [aka["value"] for aka in movie.get("properties", {}).get("akas", [])]


def guess_movie_from_description(desc, attempt=0):
    prompt = f"""
You are a movie expert AI. The user will describe an action or acting scene someone performed. Based on that description, you have to intelligently guess the movie they are trying to act out. Respond only with one likely movie name. 

Acting Description: "{desc}"

Guess the movie:
"""
    # Example LLM call
    return ask_llm_for_question({"q": prompt})  # Or call your central LLM function


