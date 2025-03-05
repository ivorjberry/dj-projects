from thefuzz import fuzz

def fuzzy_search(results, collection, playlist_name):
    # Create fuzzy file to write to
    fuzzy_file = open("fuzzy_" + playlist_name + ".txt", "w")
    fuzzy_track_count = 0
    for track in results['items']:
        artists = ", ".join(item['name'] for item in track['track']['artists'])
        
        # Check if track is in collection
        print("Checking track: " + track['track']['name'] + "; Artists: " + artists)
        
        for entry in collection:
            track_title = track['track']['name'].lower()
            entry_title = entry['title'].lower()
            if (fuzz.ratio(track_title, entry_title) > 80 or 
            track_title in entry_title or
            entry_title in track_title):
                track_artists = artists.lower()
                try:
                    entry_artists = entry['artist'].lower()
                except:
                    entry_artists = "Unknown"

                if (fuzz.ratio(track_artists, entry_artists) > 80 or
                track_artists in entry_artists or
                entry_artists in track_artists):
                    # Debug print
                    #print(f"Track: {track['track']['name']}; Artists: {artists} is in collection.")
                    #print(f"Location: {entry['location']}")
                    fuzzy_file.write(f"{entry['location']}\n")
                    fuzzy_track_count += 1
                

    print("Found " + str(fuzzy_track_count) + " tracks from playlist in collection.")
    print("FUZZY: Done checking playlist tracks in collection.")

def strict_search(results, collection, playlist_name):
    # Create strict file to write to
    strict_file = open("strict_" + playlist_name + ".txt", "w")
    track_count = 0
    for track in results['items']:
        artists = ", ".join(item['name'] for item in track['track']['artists'])
        # Debug print
        #print("Checking track: " + track['track']['name'] + "; Artists: " + artists)
        
        # Check if track is in collection
        print("Checking track: " + track['track']['name'] + "; Artists: " + artists)
        
        for entry in collection:
            if track['track']['name'] == entry['title']:
                # Debug print
                #print(f"Track: {track['track']['name']}; Artists: {artists} is in collection.")
                #print(f"Location: {entry['location']}")
                
                strict_file.write(f"Location: {entry['location']}\n")
                track_count += 1
                break

    print("Found " + str(track_count) + " tracks from playlist in collection.")
    print("STRICT: Done checking playlist tracks in collection.")