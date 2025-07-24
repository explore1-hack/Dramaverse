import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://hackathon.api.qloo.com/v2/insights"
API_KEY = os.getenv("API_KEY")

def get_movies_by_tag(tag="urn:tag:genre:media:drama"):
    headers = {
        "X-Api-Key": API_KEY
    }
    params = {
        "filter.type": "urn:entity:movie",
        "filter.tags": tag
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("results", {}).get("entities", [])
    else:
        print("Error:", response.status_code, response.text)
        return []
