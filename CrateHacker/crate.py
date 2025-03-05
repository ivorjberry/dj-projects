import tkinter as tk  
from tkinter import messagebox, filedialog
import shutil  
import os  
import re
import crate_utils as utils

#############################
# GUI utils                 #
#############################
def get_latest_version_folder(ni_directory, fallback_directory):  
    """Get the latest version folder with the name 'Traktor Pro <number>.<number>'. 
    If not found, check the .env for a saved collection location.
    If not found, return the fallback directory."""  
    try:  
        # List all directories in the base directory  
        folders = [d for d in os.listdir(ni_directory) if os.path.isdir(os.path.join(ni_directory, d))]  
          
        # Match folders that start with 'Traktor Pro ' and have a version number suffix  
        version_folders = []  
        for folder in folders:  
            match = re.match(r"Traktor Pro (\d+(\.\d+)*)", folder)  
            if match:  
                version_folders.append((folder, match.group(1)))  # (folder_name, version_string)  
  
        # Find the folder with the highest version (using natural sort for version strings)  
        if version_folders:  
            # Sort by version using a custom key to parse the version string into a tuple of integers  
            version_folders.sort(key=lambda x: tuple(map(int, x[1].split('.'))), reverse=True)  
            latest_folder = version_folders[0][0]  # Get the folder name with the highest version  
            return os.path.join(ni_directory, latest_folder)  
        else:
            print("No version folders found. Checking for saved collection location...")
            # Check current directory .env file for a saved collection location
            env_collection_location = utils.get_last_collection_location()
            if env_collection_location:
                return env_collection_location
            else:
                print("No saved collection location found. Using fallback directory.")
                return fallback_directory  
    except Exception as e:  
        print(f"Error finding latest version folder: {e}")  
        return fallback_directory  # Default to fallback directory on error    

#############################
# GUI callbacks             #
#############################

def browse_file():  
    """Open a file dialog for selecting the collection file."""  
    # Use whatever default path was determined for the collection file
    initial_directory = default_collection_filepath 
  
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
        playlist_name = utils.sp.playlist(playlist_id)['name']
        preview_label.config(text=f"Preview: {playlist_id}", fg="blue")  
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
            # Check for collection.nml in local directory
            if os.path.isfile("collection.nml"):
                collection_file = "collection.nml"
                status_label.config(text="WARNING: Using old copy of collection", fg="orange") 
            else:
                # Show a popup warning the user  
                messagebox.showerror("Invalid File", "Please select a valid .nml file.")
                status_label.config(text="Please select a valid .nml file.", fg="red")  
                return
            return
        try:
            # Copy the file to the directory where the script is running  
            destination = os.path.join(os.getcwd(), os.path.basename(collection_file))  
            shutil.copy(collection_file, destination)  
  
            # Update the status label with the copied file path and Spotify link  
            status_label.config(  
                text=f"Collection copied to: {destination}", fg="green"  
            )  
        except Exception as e:  
            # Handle any errors during the file copy  
            status_label.config(text=f"Error copying file: {e}", fg="red")  
    else:  
        # Update the status label if no file was provided  
        status_label.config(text="Please select a collection file.", fg="red")  

#############################
# GUI build in main         #
#############################

# Create the main application window  
root = tk.Tk()  
root.title("2Bays CrateHacker")  

# Get the latest version folder, or set to Documents if not found
fallback_directory = os.path.expanduser("~/Documents")  # Fallback to Documents if no version folder found
ni_base_directory = os.path.expanduser("~/Documents/Native Instruments")  # NI base directory
latest_version_folder = get_latest_version_folder(ni_base_directory, fallback_directory)  

# Set the default collection file path
if latest_version_folder == fallback_directory:  
    default_collection_filepath = fallback_directory  # Fallback to Documents 
else:
    default_collection_filepath = os.path.join(latest_version_folder, "collection.nml")  

# Collection file entry and browse button  
collection_label = tk.Label(root, text="Collection File:")  
collection_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)  

collection_entry = tk.Entry(root, width=50)  
collection_entry.grid(row=0, column=1, padx=10, pady=5)  

# Provide the dynamically determined default value  
collection_entry.insert(0, default_collection_filepath)  
  
browse_button = tk.Button(root, text="Browse", command=browse_file)  
browse_button.grid(row=0, column=2, padx=10, pady=5)  
  
# Spotify playlist link entry  
spotify_label = tk.Label(root, text="Spotify Playlist Link:")  
spotify_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)  
  
spotify_entry = tk.Entry(root, width=50)  
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
  
fuzzy_slider = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL)  
fuzzy_slider.set(80)  # Default value set to 80  
fuzzy_slider.grid(row=3, column=1, padx=10, pady=5)  

# Create Playlist button  
create_button = tk.Button(root, text="Create Playlist", command=create_playlist)  
create_button.grid(row=4, column=0, columnspan=3, pady=10)  
  
# Status label to display the entered data or status messages  
status_label = tk.Label(root, text="", fg="blue", justify=tk.LEFT)  
status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5)  
  
# Run the application  
root.mainloop()  