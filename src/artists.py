def get_followed_artists_ids(sp):
    followed_artists_ids = []
    after = None
    while True:
        response = sp.current_user_followed_artists(after=after)['artists']
        followed_artists_ids.extend(
            item['id'] for item in response['items']
        )

        if response['next'] is None:
            break

        after = followed_artists_ids[-1]

    return followed_artists_ids