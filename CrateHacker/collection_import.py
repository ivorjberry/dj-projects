import xmltodict
import os
import json

write_filename = "crate_collection"

def load_collection(file, write_json=False, write_xml=False):
    # Load collection xml into a dictionary
    with open(file, "r", encoding='utf-8') as f:
        data = f.read()
    
    collection_dict = xmltodict.parse(data)
    entries = collection_dict['NML']['COLLECTION']['ENTRY']

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
            track['location'] = entry['LOCATION']['@VOLUME'] + clean_loc(location)
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
 
    return collection

def load_fresh_collection(collection_file, crate_collection_filename):
    # Load nml collection file
    print(f"Loading fresh collection from {collection_file}...\n")
    with open(collection_file, "r", encoding='utf-8') as f:
        data = f.read()

    # Parse the xml data
    collection_dict = xmltodict.parse(data)
    entries = collection_dict['NML']['COLLECTION']['ENTRY']

    

 

def clean_loc(location):
    # Remove any leading or trailing whitespace
    location = location.strip()
    # Replace any foward slashes with backslashes
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
