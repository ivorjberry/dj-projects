import spotipy
import os
import xmltodict
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

def write_traktor_playlist(playlist_name, playlist):
    # Write the playlist to new .nml file, as xml
    with open(f"{playlist_name}.nml", "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\" ?>\n")
        f.write("<NML VERSION=\"20\"><HEAD COMPANY=\"www.native-instruments.com\" PROGRAM=\"Traktor Pro 4\"></HEAD>\n")
        f.write(f"<COLLECTION ENTRIES=\" {len(playlist)} \">\n")

        # Loop through entries, and write as xml
        for entry in playlist:
            xmltodict.unparse(entry, output=f, encoding='utf-8')
    
        # Close the collection tag and write the playlists tag
        f.write("</COLLECTION>\n")
        f.write("<SETS ENTRIES=\"0\"></SETS>")

        # Write playlist tag and nodes
        f.write("""<PLAYLISTS>
                    <NODE TYPE="FOLDER" NAME="$ROOT"><SUBNODES COUNT="1">
                    <NODE TYPE="FOLDER" NAME="2BaysCrate"><SUBNODES COUNT="1">""")

        # Write playlist node and opening tag
        f.write(f"""<NODE TYPE="PLAYLIST" NAME="{playlist_name}">
                    <PLAYLIST ENTRIES="123" TYPE="LIST">""")
        
        # Write entries for each track in playlist, combining volume, dir, and file of each entry. example:
        # <ENTRY><PRIMARYKEY TYPE="TRACK" KEY="C:/:Users/:ivorj/:Music/:iTunes/:iTunes Media/:Music/:Klaus Badelt/:Pirates of the Caribbean_ The Curse of t/:15 He's a Pirate.m4a"></PRIMARYKEY>
        # </ENTRY>
        for entry in playlist:
            entry_filename = entry['LOCATION']['@FILE']
            entry_dir = entry['LOCATION']['@DIR']
            entry_volume = entry['LOCATION']['@VOLUME']
            entry_type = "TRACK"
            if "stem.mp4" in entry_filename:
                entry_type = "STEM"
            f.write(f"""<ENTRY><PRIMARYKEY TYPE="{entry_type}" 
                        KEY="{entry_volume + entry_dir + entry_filename}"></PRIMARYKEY>\n</ENTRY>\n""")

        # Close the playlist tag and write the closing tags for the xml file
        f.write("""</PLAYLIST>\n
                    </NODE>\n
                    </SUBNODES>\n</NODE>\n
                    </SUBNODES>\n</NODE>\n
                    </PLAYLISTS>\n
                    </NML>""")
        
        print(f"Playlist {playlist_name} written to file.")
        return True