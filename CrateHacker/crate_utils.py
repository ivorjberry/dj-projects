import spotipy
import os
import json
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from collection_import import load_collection
from collection_search import strict_search, fuzzy_search



def get_playlist_id(playlist_link):
    # Extract the playlist ID from the provided link
    if "playlist/" in playlist_link:
        return playlist_link.split("playlist/")[1].split("?")[0]
    else:
        raise ValueError("Invalid Spotify playlist link.")
    
    
# Load collection into dictionary
collection_filename = "collection.nml"
collection = load_collection(collection_filename)

def get_playlist_tracks(playlist_id):
    load_dotenv()

    # Initialize Spotify API
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(client_id=os.getenv("CLIENT_ID"),
                                              client_secret=os.getenv("CLIENT_SECRET")))

    # Get playlist tracks from provided playlist id
    results = sp.playlist_tracks(playlist_id, fields="items(name,track(name,artists(name)))")
    return results


# Initialize Spotify API
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(client_id=os.getenv("CLIENT_ID"),
                                          client_secret=os.getenv("CLIENT_SECRET")))

# Get playlist tracks from provided playlist id
# https://open.spotify.com/playlist/1rB1Bn0yk4L5RKf3vqaLl8?si=777738c023bb45b3
playlist_id = "1rB1Bn0yk4L5RKf3vqaLl8"
results = sp.playlist_tracks(playlist_id, fields="items(name,track(name,artists(name)))")
playlist_name = sp.playlist(playlist_id)['name']
print(f"Checking Spotify playlist: {playlist_name}")
# Write playlist tracks to json file
with open(playlist_name + ".json", "w") as f:
    json.dump(results, f, indent=2)

strict_search(results, collection, playlist_name)
fuzzy_search(results, collection, playlist_name)