import tkinter as tk  
from tkinter import filedialog
from dotenv import set_key
import shutil  
import os
import crate_utils as utils
import collection_search as search
import collection_import as imp


#############################
# GUI callbacks             #
#############################

def browse_file():  
    """Open a file dialog for selecting the collection file."""  
    # Use whatever default path was determined for the collection file
    initial_directory = collection_entry.get() 
  
    # Open the file dialog with the latest version folder as the default  
    file_path = filedialog.askopenfilename(  
        title="Select NI Collection File",  
        initialdir=initial_directory,  
        filetypes=(("NI Collection Files", "*.nml"), ("All Files", "*.*"))  
    )  
    if file_path:  # If a file is selected, update the entry field  
        collection_entry.delete(0, tk.END)  
        collection_entry.insert(0, file_path)  


def preview_playlist():
    """Display playlist title from Spotify playlist entry."""  
    spotify_link = spotify_entry.get()  
    
    # Check if the link is provided and contains the words "spotify" and "playlist"
    if spotify_link.strip() and "spotify" in spotify_link and "playlist" in spotify_link:
        # Extract the playlist ID from the URL
        playlist_id = utils.get_playlist_id(spotify_link)
        playlist_name = utils.get_playlist_name(playlist_id)
        preview_label.config(text=f"Playlist to search: {playlist_name}", fg="blue")  
    else:  
        preview_label.config(text="Please enter a Spotify playlist link.", fg="red")  


def create_playlist():  
    """Callback function for the 'Create Playlist' button."""  
    # Get the text from the two entry fields  
    collection_file = collection_entry.get()  
    spotify_link = spotify_entry.get()  
  
    # Check if a collection file was provided  
    if collection_file:  
        # Verify provided file is of .nml type
        if not collection_file.endswith(".nml"):
            # Show a error warning the user
            status_label.config(text="Please select a valid .nml file.", fg="red")  
            return
        try:
            # Copy the file to the directory where the script is running  
            destination = os.path.join(os.getcwd(), os.path.basename(collection_file))  
            shutil.copy(collection_file, destination)  
  
            # Update the status label with the copied file path 
            status_label.config(  
                text=f"Collection copied to: {destination}", fg="green"  
            )  
        except Exception as e:  
            # Handle any errors during the file copy  
            status_label.config(text=f"Error copying file: {e}", fg="red")
            return
    else:  
        # Update the status label if no file was provided  
        status_label.config(text="Please select a collection file.", fg="red")
        return
    
    # Write last used collection file to .env
    set_key(".env", "COLLECTION_FILE", os.path.abspath(collection_file))
    
    
    # Collection now lives at destination
    status_text = status_label.cget("text") + "\nLoading collection..."
    status_label.config(text=status_text, fg="blue")
    collection, errors = imp.load_collection(destination)
    status_text = status_label.cget("text") + f"\nLoaded {len(collection)} out of {len(collection) + errors} tracks from collection."
    status_label.config(text=status_text, fg="blue")

    # Check if the link is provided and contains the words "spotify" and "playlist"
    if spotify_link.strip() and "spotify" in spotify_link and "playlist" in spotify_link:
        # Extract the playlist ID from the URL
        playlist_id = utils.get_playlist_id(spotify_link)
        playlist_name = utils.sp.playlist(playlist_id)['name']
        results = utils.get_playlist_info(playlist_id)
        
    fuzzy_ratio = fuzzy_slider.get()  
    tracks_found = search.fuzzy_search(results, collection, playlist_name, fuzzy_ratio)

    status_text = status_label.cget("text") + f"\nFound {tracks_found} tracks from playlist in collection with fuzzy ratio {fuzzy_ratio}.\nDone checking playlist tracks in collection."
    status_label.config(text=status_text, fg="blue")

#############################
# GUI build in main         #
#############################

# Create the main application window  
root = tk.Tk()  
root.title("2Bays CrateHacker")  

# Try to find latest collection file
collection_file = imp.get_collection_file()

# Collection file entry and browse button  
collection_label = tk.Label(root, text="Collection File:")  
collection_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)  

collection_entry = tk.Entry(root, width=100)  
collection_entry.grid(row=0, column=1, padx=10, pady=5)  

# Provide the dynamically determined default value  
collection_entry.insert(0, collection_file)  
  
browse_button = tk.Button(root, text="Browse", command=browse_file)  
browse_button.grid(row=0, column=2, padx=10, pady=5)  
  
# Spotify playlist link entry  
spotify_label = tk.Label(root, text="Spotify Playlist Link:")  
spotify_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)  
  
spotify_entry = tk.Entry(root, width=100)  
spotify_entry.grid(row=1, column=1, padx=10, pady=5)  

# "Preview" button  
preview_button = tk.Button(root, text="Preview", command=preview_playlist)  
preview_button.grid(row=1, column=2, padx=10, pady=5)  
  
# Label for displaying the sample text (initially blank)  
preview_label = tk.Label(root, text="", fg="blue")  
preview_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)  

# Fuzzy limit label and slider  
fuzzy_label = tk.Label(root, text="Fuzzy Limit:")  
fuzzy_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)  
  
fuzzy_slider = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL, sliderlength=60, length=400)  
fuzzy_slider.set(70)  # Default value set to 70  
fuzzy_slider.grid(row=3, column=0, columnspan=3, padx=10, pady=5)  

# Create Playlist button  
create_button = tk.Button(root, text="Create Playlist", command=create_playlist)  
create_button.grid(row=4, column=0, columnspan=3, pady=10)  
  
# Status label to display the entered data or status messages  
status_label = tk.Label(root, text="", fg="blue", justify=tk.LEFT)  
status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5)  
  
# Run the application  
root.mainloop()  