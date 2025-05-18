import aiohttp
import base64
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

async def get_spotify_token():
    async with aiohttp.ClientSession() as session:
        auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
        headers = {
            "Authorization": "Basic " + base64.b64encode(auth_str.encode()).decode()
        }
        data = {
            "grant_type": "client_credentials"
        }
        async with session.post("https://accounts.spotify.com/api/token", data=data, headers=headers) as resp:
            return (await resp.json())["access_token"]

async def search_track(track_name, token):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": track_name, "type": "track", "limit": 1}
        async with session.get("https://api.spotify.com/v1/search", headers=headers, params=params) as resp:
            data = await resp.json()

            if not data.get("tracks") or not data["tracks"]["items"]:
                return None

            item = data["tracks"]["items"][0]
            return {
                "name": item["name"],
                "artist": item["artists"][0]["name"],
                "album_cover": item["album"]["images"][0]["url"],
                "spotify_url": item["external_urls"]["spotify"]
            }
