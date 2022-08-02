import requests
from bs4 import BeautifulSoup
import spotipy
from credentials import client_id, client_secret
from spotipy.oauth2 import SpotifyOAuth

# Create an input() prompt that asks what year you would like to travel to in YYYY-MM-DD format.
user_input = input("What date would you like to travel to?\nPlease specify in the YYYY-MM-DD format.\n")
year = user_input.split("-")[0]

# Scrape the top 100 song titles on that date into a Python List
response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_input}/")
billboard_html = response.text

# Parse the song titles
soup = BeautifulSoup(billboard_html, "html.parser")
top_songs = soup.select(selector="li.o-chart-results-list__item h3.c-title")
# Make a list of songs
top_100 = [song.getText().strip() for song in top_songs]


# Create a spotipy connection
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://example.com",
    show_dialog=True,
    cache_path="token.txt"))

# Get the user ID
user_id = sp.current_user()["id"]

# Create a list of song URIs
song_uris = []
for song in top_100:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        song_uris.append(result["tracks"]["items"][0]["uri"])
        print(f"{song} was added")
    except IndexError:
        print(f"{song} doesn't exist in Spotify, skipped.")
print(song_uris)

# Create the Spotify playlist
result_playlist = sp.user_playlist_create(user=user_id, name=f"{user_input} BillBoard Top Songs", public=False)
playlist_id = result_playlist["id"]
# Add songs to the playlist
sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)

# As a result, you will have this playlist created in your Spotify account