import os
import time
import requests
from PIL import Image
from io import BytesIO

# Spotify API endpoints
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
SPOTIFY_CURRENT_TRACK_URL = f"{SPOTIFY_API_BASE_URL}/me/player/currently-playing"

# Your Spotify API access token (generate one from https://developer.spotify.com/dashboard/applications)
SPOTIFY_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# Path to the temporary image file to display
TEMP_IMAGE_FILE = "/tmp/spotify_album_art.jpg"

# Function to fetch the currently playing track's album art
def get_current_track_album_art():
    headers = {"Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"}
    response = requests.get(SPOTIFY_CURRENT_TRACK_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "item" in data and "album" in data["item"]:
            album_images = data["item"]["album"]["images"]
            if album_images:
                image_url = album_images[0]["url"]
                response = requests.get(image_url)
                if response.status_code == 200:
                    return Image.open(BytesIO(response.content))

    return None

# Function to continuously monitor and update the album art
def update_album_art():
    while True:
        album_art = get_current_track_album_art()
        if album_art:
            album_art.save(TEMP_IMAGE_FILE)
            os.system(f"feh --bg-scale {TEMP_IMAGE_FILE}")
        time.sleep(5)  # Check for updates every 5 seconds

if __name__ == "__main__":
    try:
        update_album_art()
    except KeyboardInterrupt:
        os.remove(TEMP_IMAGE_FILE)
        print("\nExiting...")