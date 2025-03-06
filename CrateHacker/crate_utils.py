import spotipy
import os
import shutil
from dotenv import load_dotenv, set_key
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
    # Get playlist tracks from provided playlist id
    results = sp.playlist_tracks(playlist_id, fields="items(name,track(name,artists(name)))")
    return results

def verify_spotify_link(spotify_link):
    # Check if the link is provided and contains the words "spotify" and "playlist"
    if spotify_link.strip() and "spotify" in spotify_link and "playlist" in spotify_link:
        return True
    else:
        return False

def verify_collection_file(collection_file) -> str:
    # Check if a collection file was provided  
    if collection_file:  
        # Verify provided file is of .nml type
        if not collection_file.endswith(".nml"):
            # Show a error warning the user
            return "Error: Please select a valid .nml file."
    else:  
        # Update the status label if no file was provided  
        return "Error: Please select a valid collection file."
    
    # Write last used collection file to .env
    set_key(".env", "COLLECTION_FILE", os.path.abspath(collection_file))
    return "Success: Valid collection file provided."