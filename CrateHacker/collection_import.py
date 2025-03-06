import xmltodict
import os
import json
import re

write_filename = "crate_collection"

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
          
        # Match folders that start with 'Traktor ' and have a version number suffix  
        version_folders = []  
        for folder in folders:  
            match = re.match(r"Traktor (\d+(\.\d+)*)", folder)  
            if match:  
                version_folders.append((folder, match.group(1)))  # (folder_name, version_string) 
  
        # Find the folder with the highest version (using natural sort for version strings)  
        if version_folders:  
            # Sort by version using a custom key to parse the version string into a tuple of integers  
            version_folders.sort(key=lambda x: tuple(map(int, x[1].split('.'))), reverse=True)  
            latest_folder = version_folders[0][0]  # Get the folder name with the highest version  
            return os.path.join(ni_directory, latest_folder)  
        else:
            print("No saved collection location found. Using fallback directory.")
            return fallback_directory  
    except Exception as e:  
        print(f"Error finding latest version folder: {e}")  
        return fallback_directory  # Default to fallback directory on error    


def get_collection_file():
    # Get the latest version folder, or set to Documents if not found
    fallback_directory = os.path.expanduser("~/Documents")  # Fallback to Documents if no version folder found
    ni_base_directory = os.path.expanduser("C:\\Users\\ivorj\\OneDrive\\Documents\\Native Instruments")  # NI base directory

    latest_version_folder = get_latest_version_folder(ni_base_directory, fallback_directory)  

    # First retry in OneDrive folder if no version folder found
    if latest_version_folder == fallback_directory:
        ni_base_directory = os.path.expanduser("~\\OneDrive\\Documents\\Native Instruments")
        latest_version_folder = get_latest_version_folder(ni_base_directory, fallback_directory)

    # If still fails to find, set the default collection file path
    if latest_version_folder == fallback_directory:
        env_collection_directory = os.getenv("COLLECTION_FILE")  # Check if collection file is saved in .env
        if env_collection_directory:
            # Set to filepath from .env
            default_collection_filepath = os.path.abspath(env_collection_directory)
        else:
            default_collection_filepath = fallback_directory  # Fallback to Documents 
    else:
        default_collection_filepath = os.path.join(latest_version_folder, "collection.nml") 

    return default_collection_filepath 


#############################
# Collection import utils   #
#############################


def load_collection(file, write_json=False, write_xml=False):
    # Load collection xml into a dictionary
    with open(file, "r", encoding='utf-8') as f:
        data = f.read()
    
    collection_dict = xmltodict.parse(data)
    entries = collection_dict['NML']['COLLECTION']['ENTRY']
    
    return entries
"""
    # Create a dictionary for each track in the collection
    collection = []
    total_errors = 0
    for entry in entries:
        try:
            track = {}
            track['title'] = entry['@TITLE']
            # Artist might not exist for some tracks
            if '@ARTIST' in entry:           
                track['artist'] = entry['@ARTIST']
            # Clean up location string to standardize
            location = entry['LOCATION']['@DIR'] + entry['LOCATION']['@FILE']
            track['location'] = entry['LOCATION']['@VOLUME'] + clean_location(location)
            collection.append(track)
        except:
            if total_errors == 0:
                print("Error loading tracks from collection.") 
                # Delete old error file
                if os.path.exists("error.txt"):
                    os.remove("error.txt")
            
            total_errors += 1
            # Write to error file
            with open("error.txt", "a") as ef:
                ef.write(f"Error writing track to file: " + entry['@TITLE'] + "\n")
        
    print(f"Loaded {len(collection)} out of {len(entries)} tracks from collection.\n")
    if total_errors > 0:
            print(f"Total errors: {total_errors}")

    print("Done loading collection.\n")

    # Write track title, artist, and location
    if write_json:
        write_json(collection)
    
    if write_xml:
        write_xml(collection)    
 
    return collection, total_errors
"""
def clean_location(location):
    # Remove any leading or trailing whitespace
    location = location.strip()
    # Replace any backslashes with forward slashes
    #location = location.replace("/", "\\")
    # Remove any colons put in by traktor
    location = location.replace(":", "")
    return location

def write_json(collection):
    filename = write_filename + ".json"

    # Delete the json file if it exists
    if os.path.exists(filename):
        os.remove(filename)
        
    # Write track title, artist, and location from entries to json file
    with open("collection.json", "w") as f:
        json.dump(collection, f, indent=2)
    print("Wrote collection to json file.\n")

def write_xml(collection):
    filename = write_filename + ".xml"

    # Delete the xml file if it exists
    if os.path.exists(filename):
        os.remove(filename)
    
    # Write track title, artist, and location from entries to xml file
    with open("collection.xml", "w", encoding='utf-8') as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<COLLECTION>")
        for track in collection:
            f.write(f"<TRACK TITLE=\"{track['title']}\" ARTIST=\"{track['artist']}\" LOCATION=\"{track['location']}\">")
            f.write(f"</TRACK>\n")
        f.write("</COLLECTION>\n")
    print("Wrote collection to xml file.\n")
