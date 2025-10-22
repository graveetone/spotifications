from dotenv import load_dotenv

from proxy import get_spotify_proxy
from clients.spotipy_client import SpotipyClient

load_dotenv()

target_playlist_id = "5p0Q2yU0Evpy0jMZju8Hei"
spotipy_client = SpotipyClient(spotipy_client=get_spotify_proxy())

duplicates = spotipy_client.get.get_playlist_duplicates(playlist_id=target_playlist_id)


# import pickle
# pickle.dump(duplicates, open("dups", "wb")) # dump duplicates
# duplicates = pickle.load(open("dups", "rb")) # restore duplicates

for track_name, track_ids in duplicates.items():
    track = spotipy_client.get.get_track(track_ids[0])
    print("Track:")
    print("Name:", track["name"])
    print("Artists:", [a['name'] for a in track["artists"]])
    print("Album:", track["album"]["name"])
    print(f"Duplicates ({len(track_ids[1:])}):", track_ids[1:])

    for track_id in track_ids[1:]:
        track = spotipy_client.get.get_track(track_id)
        print("Name:", track["name"])
        print("Artists:", [a["name"] for a in track["artists"]])
        print("Album:", track["album"]["name"])
        print("URI:", track["uri"])

        drop = input("Drop? (y/n)")
        if drop == "y":
            spotipy_client.post.delete_track(playlist_id=target_playlist_id, track_id=track_id)
            print("Deleted")
