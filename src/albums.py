import datetime

def get_artists_albums(artist_id, newer_than=None):
    print(f"Releases for {artist_id}")
    if newer_than is None:
        newer_than = datetime.datetime.now()
    artists_albums = []
    offset = 0
    while True:
        response = sp.artist_albums(artist_id=artist_id, offset=offset, include_groups="album,single,compilation")
        for release in response['items']:
            release_date = release['release_date']
            if len(release_date) == 4:
                release_date += "-01-01"
            release_date = datetime.datetime.fromisoformat(release_date)

            if release_date > newer_than:
                artists = ", ".join(artist['name'] for artist in release['artists'])
                artists_albums.append(
                    f"{artists} - {release['name']}"
                )
        print(f"New albums: {artists_albums}")
        print(response['next'])
        if response['total'] <= offset:
            break

        offset += response['limit']

    return artists_albums