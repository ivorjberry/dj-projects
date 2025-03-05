import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# Initialize Spotify API globally
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(client_id=os.getenv("CLIENT_ID"),
                                            client_secret=os.getenv("CLIENT_SECRET")))

def get_playlist_id(playlist_link):
    # Extract the playlist ID from the provided link
    if "playlist/" in playlist_link:
        return playlist_link.split("playlist/")[1].split("?")[0]
    else:
        raise ValueError("Invalid Spotify playlist link.")
    
def get_playlist_name(playlist_id):
    # Get playlist name from provided playlist id
    return sp.playlist(playlist_id)['name']

def get_playlist_info(playlist_id):
    load_dotenv()

    # Get playlist tracks from provided playlist id
    results = sp.playlist_tracks(playlist_id, fields="items(name,track(name,artists(name)))")
    return results

