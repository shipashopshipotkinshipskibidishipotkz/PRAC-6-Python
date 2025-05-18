import aiohttp
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

async def search_lyrics_url(song_title, artist):
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    search_url = "https://api.genius.com/search"
    params = {"q": f"{song_title} {artist}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers, params=params) as resp:
            data = await resp.json()
            for hit in data["response"]["hits"]:
                if artist.lower() in hit["result"]["primary_artist"]["name"].lower():
                    return hit["result"]["url"]
            return None

async def search_by_lyrics_snippet(snippet):
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    search_url = "https://api.genius.com/search"
    params = {"q": snippet}

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers, params=params) as resp:
            data = await resp.json()
            if data["response"]["hits"]:
                hit = data["response"]["hits"][0]["result"]
                return hit["title"], hit["primary_artist"]["name"]
            return None, None
